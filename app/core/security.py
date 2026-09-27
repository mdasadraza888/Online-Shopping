from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.token import TokenData
from app.core.config import settings


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto"
)

ALGORITHM = 'HS256'
EXPIRY_TIME = settings.EXPIRY_TIME

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
        expiry = datetime.now(timezone.utc) + timedelta(minutes=EXPIRY_TIME)

    to_encode.update({'exp': expiry})
    my_token = jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)
    return my_token

my_token = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(db: Session, token: str = Depends(my_token)):
    from app.crud.crud_user import get_user

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        email: str = payload.get('email')
        role: str = payload.get('role')

        if not username:
            raise
        user = TokenData(name=username, email=email, role=role)
    except JWTError:
        raise
    user = get_user(db, email=email)
    if not user:
        raise
    return user