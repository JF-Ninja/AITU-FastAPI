from asyncio.log import logger
import random
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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
verification_codes = {}

def send_email(to_email, verification_code):
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login("eserikova22@gmail.com", "zokthaldgnrnfjtw")

    msg = MIMEMultipart()
    msg["From"] = "eserikova22@gmail.com"
    msg["To"] = to_email
    msg["Subject"] = "Код верификации"

    text = f"Ваш код верификации: {verification_code}"
    msg.attach(MIMEText(text, "plain"))

    smtp_server.sendmail("eserikova22@gmail.com", to_email, msg.as_string())
    smtp_server.quit()

class check_email(BaseModel):
    email: str
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
class VerifyRequest(BaseModel):
    email: str
    verification_code: int
class ChangePassword(BaseModel):
    email: str
    new_password: str

class NewClass(BaseModel):
    new_info: str

@app.post("/Registration")
async def Registration(user: Registration):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM users WHERE user_email = $1"
        row = await conn.fetchrow(query, user.email)
        if row:
            raise HTTPException(status_code=401, detail="Login exists")
        else:
            hashed_password = pwd_context.hash(user.password)
            query_insert_user_data = """
                        INSERT INTO users(user_name, user_surname, user_email, password_hash, user_role, gender)
                        VALUES($1, $2, $3, $4, $5, $6);
                    """
            await conn.execute(query_insert_user_data, user.name, user.surname, user.email, hashed_password, user.role,
                               user.gender)
            to_encode = {"login": user.email, "exp": datetime.utcnow() + EXPIRATION_TIME}
            token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            return {"message": "registration successful", "detail": "created new user", "token": token}
    finally:
        if conn:
            await conn.close()


@app.post("/check_login")
async def check_login(user: check_login):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM users WHERE user_email = $1"
        row = await conn.fetchrow(query, user.email)

        if row:
            if pwd_context.verify(user.password, row['password_hash']):
                to_encode = {"login": user.email, "exp": datetime.utcnow() + EXPIRATION_TIME}
                token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
                return {"message": "Login successful", "detail": "Verified", "token": token}
            else:
                raise HTTPException(status_code=401, detail="Incorrect password")
        else:
            raise HTTPException(status_code=401, detail="Incorrect email")

    finally:
        if conn:
            await conn.close()


@app.post("/check_email")
async def check_email(user: check_email):
    conn = None
    try:
        conn = await get_database_connection()
        query = "SELECT * FROM users WHERE user_email = $1"
        row = await conn.fetchrow(query, user.email)

        if row:
            verification_code = random.randint(1000, 9999)
            verification_codes[user.email] = verification_code
            send_email(user.email, verification_code)
            return {"message": "Login checked", "detail": "Verified", "verification_code": verification_code}
        else:
            raise HTTPException(status_code=401, detail="Incorrect email")
    finally:
        if conn:
            await conn.close()


@app.post("/verify_code")
async def verify_code(request: VerifyRequest):
    stored_code = verification_codes.get(request.email)
    if stored_code is None:
        raise HTTPException(status_code=404, detail="Verification code not found for this email")
    if stored_code != request.verification_code:
        raise HTTPException(status_code=400, detail="Incorrect verification code")
    return {"message": "Verification successful"}

@app.post("/change_password")
async def change_password(request: ChangePassword):
    conn = None
    try:
        conn = await get_database_connection()
        hashed_password = pwd_context.hash(request.new_password)

        query_update_password = """UPDATE users SET password_hash = $1 WHERE user_email = $2;"""
        await conn.execute(query_update_password, hashed_password, request.email)
        to_encode = {"login": request.email, "exp": datetime.utcnow() + EXPIRATION_TIME}

        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return {"message": "Password updated successfully", "token": token}
    finally:
        if conn:
            await conn.close()

@app.post("/new_request")
async def new_request(info: NewClass):
    conn = None
    try:
        conn = await get_database_connection()

        query_update_password = """INSERT INTO some_info(cards)
            VALUES($1)"""
        await conn.execute(query_update_password, info.new_info)
        return {"message": "new info is ok"}
    finally:
        if conn:
            await conn.close()