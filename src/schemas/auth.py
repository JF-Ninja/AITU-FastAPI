from pydantic import BaseModel, EmailStr

class Registration(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    role: str
    gender: str