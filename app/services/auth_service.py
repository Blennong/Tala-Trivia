# app/services/auth_service.py
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from app.jwt_config import settings 

def hash_password(password: str) -> str:
	return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
	to_encode = data.copy()
	expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
	return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
	try:
		payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
		return payload
	except JWTError:
		return None
