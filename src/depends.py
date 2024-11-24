from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import UserService
from repositories.auth import UserRepository
from database import get_db

async def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(UserRepository(db))
