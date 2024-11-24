from fastapi import APIRouter, Depends, HTTPException
from schemas.auth import Registration
from services.auth import UserService
from depends import get_user_service

router = APIRouter(prefix="/registration", tags=["registration"])


# Creating new user
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


# Check if the user data correct for SignIn
router = APIRouter(prefix="/authorization", tags=["authorization"])
@router.post("", description="Check the user's account")
async def check_user(
    user: Registration,
    user_service: UserService = Depends(get_user_service)
):
    try:
        result = await user_service.check_user(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


