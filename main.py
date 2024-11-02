from asyncio.log import logger
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
import asyncpg
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from typing import Dict
connected_clients: Dict[str, WebSocket] = {}

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = timedelta(minutes=int(os.getenv("EXPIRATION_TIME_MINUTES")))
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_database_connection():
    return await asyncpg.connect(DATABASE_URL)

class UserLogin(BaseModel):
    login: str
    password: str
    avatar: str
    email: str
    roll: str
    gender: str



@app.post("/check_login")
async def check_login(user: UserLogin):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM users WHERE login = $1"
        row = await conn.fetchrow(query, user.login)

        if row:
            to_encode = {"login": user.login, "exp": datetime.utcnow() + EXPIRATION_TIME}
            token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return {"message": "Login exists", "access_token": token}
        else:
            raise HTTPException(status_code=401, detail="Incorrect login")

    finally:
        if conn:
            await conn.close()