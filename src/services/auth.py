from random import randint
from passlib.context import CryptContext
import aioredis
from repositories.auth import UserRepository
from services.token import TokenRepository
from services.email_verification import EmailService
from schemas.auth import Registration, AuthLogin, AuthData, VerifyRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

recovery_codes = {}

class UserService:
    def __init__(self, repository: UserRepository, token_repository: TokenRepository, email_service: EmailService):
        self.redis_client = None
        self.repository = repository
        self.token_repository = token_repository
        self.email_service = email_service
        self.redis_client = self.redis_client

    async def register_user(self, user: Registration):
        existing_user = await self.repository.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = pwd_context.hash(user.password)
        await self.repository.create_user(user, hashed_password)

        token = self.token_repository.encode_token(user.email)

        return {"message": "Registration successful", "token": token}

    async def check_user(self, user: AuthData):
        existing_user = await self.repository.get_user_by_email(user.email)
        if not existing_user:
            raise ValueError("User with this email is not registered")

        if not pwd_context.verify(user.password, existing_user.password_hash):
            raise ValueError("Incorrect password")

        token = self.token_repository.encode_token(user.email)

        return {"message": "SignIn successful", "token": token}

    async def recover_user(self, user: AuthLogin):
        existing_user = await self.repository.get_user_by_email(user.email)
        if not existing_user:
            raise ValueError("Пользователь с таким email не найден")

        verification_code = randint(100000, 999999)

        await self.email_service.send_email(user.email, verification_code)

        expiration_time = 10 * 60
        await self.redis_client.setex(user.email, expiration_time, verification_code)

        return {"message": "Код восстановления отправлен на email"}

    async def verify_code(self, user: VerifyRequest):

        stored_code = await self.redis_client.get(user.email)

        if not stored_code:
            raise ValueError("Запрос на восстановление не найден для этого email")

        if int(user.verification_code) != int(stored_code):
            raise ValueError("Неверный код восстановления")

        await self.redis_client.delete(user.email)
        return {"message": "Код восстановления действителен"}