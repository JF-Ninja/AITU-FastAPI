from fastapi import APIRouter, Depends, HTTPException
from src.schemas.auth import Registration
from src.services.auth import UserService
from src.depends import get_database
import asyncpg

router = APIRouter(prefix="/registration", tags=["registration"])

@router.post("", description="Register a new user")
async def register_user(
    user: Registration,
    connection: asyncpg.Connection = Depends(get_database)
):
    try:
        user_service = UserService(connection)
        result = await user_service.register_user(user)
        return result
    except HTTPException as e:
        raise e
