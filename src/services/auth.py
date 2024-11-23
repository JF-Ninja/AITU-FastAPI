from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
import os
from src.schemas.auth import Registration
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = timedelta(minutes=int(os.getenv("EXPIRATION_TIME_MINUTES")))

class UserService:
    def __init__(self, repository):
        self.repository = repository

    async def register_user(self, user: Registration):
        existing_user = await self.repository.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = pwd_context.hash(user.password)
        await self.repository.create_user(user, hashed_password)

        to_encode = {"email": user.email, "exp": datetime.utcnow() + EXPIRATION_TIME}
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"message": "Registration successful", "detail": "Created new user", "token": token}
