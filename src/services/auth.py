from random import randint
from passlib.context import CryptContext
from datetime import datetime, timedelta
from repositories.auth import UserRepository
from services.token import TokenRepository
from services.email_verification import EmailService
from schemas.auth import Registration, AuthLogin, AuthData, VerifyRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository, token_repository: TokenRepository, email_service: EmailService):
        self.repository = repository
        self.token_repository = token_repository
        self.email_service = email_service
        self.recovery_codes = {}

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
        expiration_time = datetime.utcnow() + timedelta(minutes=10)

        self.recovery_codes[user.email] = {
            "verification_code": verification_code,
            "expiration_time": expiration_time
        }
        return {"message": "Код восстановления отправлен на email"}

    """async def verify_recovery_code(self, user: VerifyRequest):

        saved_code_data = self.recovery_codes.get(user.email)
        if not saved_code_data:
            raise ValueError("Запрос на восстановление не найден для этого email")

        saved_code = saved_code_data["verification_code"]
        expiration_time = saved_code_data["expiration_time"]

        if user.verification_code != saved_code:
            raise ValueError("Неверный код восстановления")
        if datetime.utcnow() > expiration_time:
            del self.recovery_codes[user.email]
            raise ValueError("Код восстановления истек")

        del self.recovery_codes[user.email]
        return {"message": "Код восстановления действителен"}"""