import asyncpg
import os
from fastapi import Depends
from repositories.auth import UserRepository
from services.auth import UserService

class Database:
    _pool = None

    @classmethod
    async def connect(cls):
        if not cls._pool:
            cls._pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
        return cls._pool

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None

async def get_database():
    pool = await Database.connect()
    async with pool.acquire() as conn:
        yield conn

async def get_user_service(connection: asyncpg.Connection = Depends(get_database)):
    return UserService(UserRepository(connection))