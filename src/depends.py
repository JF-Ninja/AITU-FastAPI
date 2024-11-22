from src.repositories.auth import UserRepository
from src.services.auth import UserService
import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_database_connection():
   return await asyncpg.connect(DATABASE_URL)

async def get_user_service():
    conn = await get_database_connection()
    repository = UserRepository(conn)
    return UserService(repository)
