from passlib.context import CryptContext
from repositories.auth import UserRepository
from repositories.token import TokenRepository
from schemas.auth import Registration

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository, token_repository: TokenRepository):
        self.repository = repository
        self.token_repository = token_repository

    async def register_user(self, user: Registration):
        existing_user = await self.repository.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = pwd_context.hash(user.password)
        await self.repository.create_user(user, hashed_password)

        token = self.token_repository.encode_token(user.email)

        return {"message": "Registration successful", "token": token}

