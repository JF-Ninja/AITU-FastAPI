from asyncio.log import logger
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class check_login(BaseModel):
    email: str
    password: str
class Registration(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    role: str
    gender: str
@app.post("/Registration")
async def Registration(user: Registration):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM users WHERE user_email = $1"
        row = await conn.fetchrow(query, user.email)
        if row:

            return {"success": False, "detail": "Login exists"}
        else:
            hashed_password = pwd_context.hash(user.password)
            query_insert_user_data = """
                        INSERT INTO users(user_name, user_surname, user_email, password_hash, user_role, gender)
                        VALUES($1, $2, $3, $4, $5, $6);
                    """
            await conn.execute(query_insert_user_data, user.name, user.surname, user.email, hashed_password, user.role,
                               user.gender)
            return {"success": True, "detail": "user created successfully"}
    finally:
        if conn:
            await conn.close()

@app.post("/check_login")
async def check_login(user: check_login):
    conn = None
    try:
        conn = await get_database_connection()
        hashed_password = pwd_context.hash(user.password)
        query = "SELECT * FROM users WHERE login = $1 AND password = $2"
        row = await conn.fetchrow(query, user.email, hashed_password)

        if row:
            return {"success": True, "detail": "Verified"}
        else:
            return {"success": False, "detail": "Incorrect login or password"}

    finally:
        if conn:
            await conn.close()