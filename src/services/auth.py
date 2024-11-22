from src.repositories.auth import UserRepository
from src.schemas.auth import Registration
from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = timedelta(minutes=int(os.getenv("EXPIRATION_TIME_MINUTES")))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user: Registration):
        existing_user = await self.repository.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=401, detail="Login exists")

        hashed_password = pwd_context.hash(user.password)
        await self.repository.create_user(user, hashed_password)

        to_encode = {"login": user.email, "exp": datetime.utcnow() + EXPIRATION_TIME}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"message": "Registration successful", "detail": "Created new user", "token": token}
