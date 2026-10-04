"""
Security utilities: Password Hashing and JWT tokens
"""
import datetime
from typing import Optional, Dict, Any
import jwt
import hashlib
import secrets
from app.core.config import settings

def hash_password(password: str) -> str:
    # Use standard library PBKDF2-HMAC-SHA256 for zero-dependency reliability
    salt = secrets.token_hex(16)
    pwd_bytes = password.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt.encode('utf-8'), 100000)
    return f"pbkdf2_sha256$100000${salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    try:
        # 1. Try bcrypt if hash starts with $2b$ or $2a$
        if hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"):
            try:
                import bcrypt
                pwd_bytes = plain_password.encode('utf-8')[:72]
                hash_bytes = hashed_password.encode('utf-8')
                if bcrypt.checkpw(pwd_bytes, hash_bytes):
                    return True
            except Exception:
                pass
            try:
                from passlib.context import CryptContext
                ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
                if ctx.verify(plain_password[:72], hashed_password):
                    return True
            except Exception:
                pass

        # 2. Try PBKDF2 format
        parts = hashed_password.split("$")
        if len(parts) == 4 and parts[0] == "pbkdf2_sha256":
            iterations = int(parts[1])
            salt = parts[2]
            expected_key = parts[3]
            computed = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), iterations)
            return secrets.compare_digest(computed.hex(), expected_key)
    except Exception:
        pass
    return False

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
