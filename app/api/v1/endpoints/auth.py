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
from app.core import exceptions
from app.api.deps import decode_token, role_checker
from app.core import redis
from app.services import email_service

router = APIRouter()

@router.post("/api/v1/endpoints/auth/sign-up", response_model=UserResponse)
async def register(user: UserRequest, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db=db, email=user.email)

        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")


        new_user = create_user(db=db, user=user)

        return new_user
    except:
        db.rollback()
        raise exceptions.AuthenticationException("Server error.")

@router.post("/api/v1/endpoints/auth/login", response_model=Token)
async def login_to_access_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        db_user = authentication_user(db=db, email=form.username, password=form.password)

        if not db_user:
            raise exceptions.AuthenticationException("Credential are invalid!")

        if not role_checker():
            raise exceptions.AuthenticationException("Role are mismatch.")

        access_token = create_access_token(data={'sub': db_user.email, 'role': db_user.role.value})
        refreh_token = create_refresh_token(data={'sub': db_user.email, 'role': db_user.role.value})

        #otp = await email_service.send_email(form.email)

        

        return {"access_token": access_token, "refresh_token": refreh_token, "token_type": "bearer"}
    except:
        db.rollback()
        raise exceptions.AuthenticationException("Server error.")

@router.post("/api/v1/endpoints/auth/refresh_token/", response_model=RefreshTokenResponse)
def new_access_token(refresh_token: str):
    try:
        payload = decode_token(token=refresh_token)

        token_type = payload.get('type')
        role = payload.get("role")

        if token_type != 'refresh':
            raise exceptions.AuthenticationException("Invalid token type. Expected a refresh token.") 

        email =  payload.get("sub")

        if not email:
            raise exceptions.AuthenticationException("Invalid token payload. Missing 'email' claim.")

        new_access_token = create_access_token(data={'sub': email, "role": role})
        return {"access_token": new_access_token, "token_type": "Bearer"}
    except JWTError:
        raise exceptions.AuthenticationException("Invalid refresh token.")

@router.post("/api/v1/endpoints/auth/logout")
def logout(refresh_token: str):
    payload = decode_token(token=refresh_token)
    jti = payload.get("jti")

    if not jti:
        raise exceptions.AuthenticationException("Invalid request for logout")

    redis.revoke_token(jti=jti, expires_in=settings.EXPIRY_TIME)

    return {'status': "success", "message": "Logout Successfully."}

@router.post("/api/v1/endpoints/auth/verification")
async def verification_account(otp: str):
    return otp