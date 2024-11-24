from pydantic import BaseModel

class Registration(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    role: str
    gender: str

class AuthLogin(BaseModel):
    email: str
    password: str