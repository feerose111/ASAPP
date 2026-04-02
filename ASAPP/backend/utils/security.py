from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from fastapi.security import HTTPBearer
import uuid

from config import settings

oauth2_scheme = HTTPBearer(auto_error=True)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------- PASSWORD UTILS ----------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------- JWT TOKEN CREATION ----------------------
def create_access_token(data: dict, expiry: Optional[timedelta] = None, refresh: bool= False) -> str:
    payload=data.copy()
    payload.update({
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)),
        'jti': str(uuid.uuid4()),
        'refresh' : refresh
    })
    encoded_jwt = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
        )
    return encoded_jwt