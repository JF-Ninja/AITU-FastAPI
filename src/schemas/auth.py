from pydantic import BaseModel

class Registration(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    role: str
    gender: str

class AuthData(BaseModel):
    email: str
    password: str

class AuthLogin(BaseModel):
    email: str

class VerifyRequest(BaseModel):
    email: str
    verification_code: int