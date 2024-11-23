import os
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Constants for JWT
SECRET_KEY = os.getenv('SECRET_KEY', '')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password, scheme="bcrypt")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token:str) -> str:
    try:
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get('sub')
        if user_email is None:
            raise HTTPException(status_code=400, detail='Invalid token')
        return user_email
    except Exception as e:
        raise HTTPException(status_code=400, detail='Invalid token')
