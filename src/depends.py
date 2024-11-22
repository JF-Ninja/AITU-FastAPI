from fastapi import Depends
import asyncpg
import os

class Database:
    def __init__(self):
        self._database_url = os.getenv("DATABASE_URL")
        self._connection = None

    async def connect(self):
        if not self._connection:
            self._connection = await asyncpg.connect(self._database_url)
        return self._connection

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None

async def get_database() -> asyncpg.Connection:
    db = Database()
    conn = await db.connect()
    try:
        yield conn
    finally:
        await db.close()
