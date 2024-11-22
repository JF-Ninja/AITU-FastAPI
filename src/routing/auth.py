from fastapi import APIRouter, Depends, HTTPException
from src.schemas.auth import Registration
from src.services.auth import UserService
from src.depends import get_user_service

router = APIRouter(prefix="/registration", tags=["registration"])

@router.post("", description="Регистрация нового пользователя")
async def register_user(
    user: Registration,
    user_service: UserService = Depends(get_user_service)
):
    try:
        result = await user_service.register_user(user)
        return result
    except HTTPException as e:
        raise e
    finally:
        await user_service.repository.conn.close()
