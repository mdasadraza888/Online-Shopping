from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserRequest, UserResponse
from app.crud.crud_user import get_user, create_user
from app.schemas.token import Token, RefreshTokenResponse
from app.core.database import get_db
from app.core.security import create_access_token, verify_hashed_password, authentication_user, create_refresh_token
from jose import jwt, JWTError
from app.core.config import settings

router = APIRouter()

@router.post("/Sign-up", response_model=UserResponse)
def register(user: UserRequest, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db=db, email=user.email)

        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

        new_user = create_user(db=db, user=user)
        return new_user
    except:
        db.rollback()
        raise

@router.post("/api/v1/endpoints/auth/login", response_model=Token)
def login_to_access_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        db_user = authentication_user(db=db, email=form.username, password=form.password)

        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        access_token = create_access_token(data={'sub': db_user.email, 'role': db_user.role.value})
        refreh_token = create_refresh_token(data={'sub': db_user.email, 'role': db_user.role.value})

        return {"access_token": access_token, "refresh_token": refreh_token, "token_type": "bearer"}
    except:
        db.rollback()
        raise

@router.post("/api/v1/endpoints/auth/refresh_token", response_model=RefreshTokenResponse)
def new_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        token_type = payload.get('type')
        role = payload.get("role")

        if token_type != 'refresh':
            raise HTTPException(
                status_code=401,
                detail="invalid refresh token"
            )

        email =  payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=401,
                detail="invalid refresh token"
            )

        new_access_token = create_access_token(data={'sub': email, "role": role})
        return {"access_token": new_access_token, "token_type": "Bearer"}
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

@router.post("api/v1/endpoints/auth/logout")
def logout(current_user = Depends(get_db)):
    pass