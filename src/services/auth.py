from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import Registration
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from services.auth import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = timedelta(minutes=int(os.getenv("EXPIRATION_TIME_MINUTES")))

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user: Registration):
        existing_user = await self.repository.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = pwd_context.hash(user.password)
        await self.repository.create_user(user, hashed_password)

        token_data = {"email": user.email, "exp": datetime.utcnow() + EXPIRATION_TIME}
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

        return {"message": "Registration successful", "token": token}

