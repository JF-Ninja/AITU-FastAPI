from fastapi import APIRouter, Depends, HTTPException
from schemas.auth import Registration, AuthLogin, AuthData, VerifyRequest
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



router1 = APIRouter(prefix="/authorization", tags=["authorization"])


# Check if the user data correct for SignIn
@router.post("", description="Check the user's account")
async def check_user(
    user: AuthData,
    user_service: UserService = Depends(get_user_service)
):
    try:
        result = await user_service.check_user(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



router2 = APIRouter(prefix="/recovery", tags=["recovery"])

@router.post("", description="Recover the user's account")

async def recover_user(
    user: AuthLogin,
    user_service: UserService = Depends(get_user_service)
):
    try:
        result = await user_service.recover_user(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


router3 = APIRouter(prefix="/verify_code", tags=["verify_code"])
@router.post("", description="Verify the recovery code")


async def verify_code(
    user: VerifyRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        result = await user_service.verify_recovery_code(user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))