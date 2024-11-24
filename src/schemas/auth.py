from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_surname = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    user_role = Column(String, nullable=False)
    gender = Column(String, nullable=False)