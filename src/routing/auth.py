from fastapi import APIRouter, Depends, HTTPException

from repositories.auth import UserRepository
from schemas.auth import Registration
from services.auth import UserService
from depends import get_database, get_user_service

import asyncpg

router = APIRouter(prefix="/registration", tags=["registration"])

@router.post("", description="Register a new user")
async def register_user(
    user: Registration,
    user_service: UserService = Depends(get_user_service)
):
    try:
        result = await user_service.register_user(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

