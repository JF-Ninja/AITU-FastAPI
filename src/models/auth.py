from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "USERS"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    user_surname = Column(String(100), nullable=False)
    user_email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    profile_image = Column(String(255))
    user_role = Column(String(50), nullable=False)
    region = Column(String(255))
    gender = Column(String(10))
    created_at = Column(DateTime, default=func.now())