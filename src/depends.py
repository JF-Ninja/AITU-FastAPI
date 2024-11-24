from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import UserService
from repositories.auth import UserRepository
from services.token import TokenRepository
from database import get_db
from services.email_verification import EmailService

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    token_repository = TokenRepository()
    email_service = EmailService
    return UserService(UserRepository(db), token_repository, email_service)
