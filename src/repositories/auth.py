from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from models import User
from schemas.auth import Registration

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.user_email == email))
        return result.scalars().first()

    async def create_user(self, user: Registration, hashed_password: str):
        new_user = User(
            user_name=user.name,
            user_surname=user.surname,
            user_email=user.email,
            password_hash=hashed_password,
            user_role=user.role,
            gender=user.gender
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)