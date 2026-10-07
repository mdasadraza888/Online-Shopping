from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.token import TokenData
from app.core.config import settings
from uuid import uuid4


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto"
)



def get_hash_password(password: str):
    return pwd_context.hash(password)

def verify_hashed_password(normal_password, hashed_password):
    return pwd_context.verify(normal_password, hashed_password)

def authentication_user(db: Session, email: str, password: str):
    from app.crud.crud_user import get_user

    db_user = get_user(db=db, email=email)
    if not db_user:
        return False
    if not verify_hashed_password(password, db_user.password_hash):
        return False

    return db_user

def create_access_token(data: dict, expiry_time: timedelta | None = None):
    to_encode = data.copy()
    if expiry_time is not None:
        expiry = datetime.now(timezone.utc) + expiry_time
    else:
        expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.EXPIRY_TIME)

    to_encode.update({'jti': str(uuid4()), 'exp': expiry, 'type': 'access'})
    my_token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return my_token

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({'jti': str(uuid4()), 'exp': expire, 'type': 'refresh'})

    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return refresh_token





























































