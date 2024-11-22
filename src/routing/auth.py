from fastapi import APIRouter, Depends, HTTPException

from src.repositories.auth import UserRepository
from src.schemas.auth import Registration
from src.services.auth import UserService
from src.depends import get_database
import asyncpg

router = APIRouter(prefix="/registration", tags=["registration"])

@router.post("", description="Register a new user")
async def register_user(
    user: Registration,
    connection: asyncpg.Connection = Depends(get_database)):
    user_service = UserService(UserRepository(connection))
    try:
        result = await user_service.register_user(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

