from fastapi import APIRouter, Depends, HTTPException
from schemas.auth import Registration
from services.auth import UserService
from depends import get_user_service

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


