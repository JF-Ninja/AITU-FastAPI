import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = timedelta(minutes=int(os.getenv("EXPIRATION_TIME_MINUTES")))

class TokenRepository:
    @staticmethod
    def encode_token(email: str) -> str:
        token_data = {
            "email": email,
            "exp": datetime.utcnow() + EXPIRATION_TIME
        }
        token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return token
