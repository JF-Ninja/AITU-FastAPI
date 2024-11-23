from typing import Optional
from schemas.auth import Registration
import asyncpg

class UserRepository:
    def __init__(self, connection: asyncpg.Connection):
        self.conn = connection

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        query = "SELECT * FROM users WHERE user_email = $1"
        return await self.conn.fetchrow(query, email)

    async def create_user(self, user: Registration, hashed_password: str):
        query_insert_user_data = """
            INSERT INTO users(user_name, user_surname, user_email, password_hash, user_role, gender)
            VALUES($1, $2, $3, $4, $5, $6);
        """
        await self.conn.execute(
            query_insert_user_data,
            user.name, user.surname, user.email, hashed_password, user.role, user.gender
        )
