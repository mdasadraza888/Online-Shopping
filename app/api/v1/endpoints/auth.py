from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserRequest, UserResponse, UserUpdate
from app.crud import crud_user
from app.schemas.token import Token, RefreshTokenResponse
from app.core.database import get_db
from app.core import security
from jose import jwt, JWTError
from app.core.config import settings
from app.core import exceptions
from app.api.deps import decode_token, role_checker, get_current_user
from app.core import redis
from app.services import email_service

router = APIRouter()

@router.post("/api/v1/endpoints/auth/sign-up", response_model=UserResponse)
async def register(user: UserRequest, background_taks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        db_user = crud_user.get_user(db=db, email=user.email)

        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

        new_user = crud_user.create_user(db=db, user=user)

        background_taks.add_task(await email_service.send_email(email=user.email, username=user.name))
        

        return new_user
    except:
        db.rollback()
        raise exceptions.AuthenticationException("Server error.")

@router.post("/api/v1/endpoints/auth/login", response_model=Token)
async def login_to_access_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        db_user = security.authentication_user(db=db, email=form.username, password=form.password)

        if not db_user:             
            raise exceptions.AuthenticationException(db_user)

        if not role_checker():
            raise exceptions.AuthenticationException(db_user)

        access_token = security.create_access_token(data={'sub': db_user.email, 'role': db_user.role.value})
        refresh_token = security.create_refresh_token(data={'sub': db_user.email, 'role': db_user.role.value})

        otp = await email_service.send_otp_email(email=db_user.email, username=db_user.name)

        if not otp:
            raise exceptions.AuthenticationException("Invalid otp.")

        otp_token = security.create_otp_token(data={'sub': db_user.email, 'otp': otp})

    
        return {"access_token": access_token, "refresh_token": refresh_token, "otp_token": otp_token, "token_type": "bearer"}
    except:
        db.rollback()
        raise 

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

        new_access_token = security.create_access_token(data={'sub': email, "role": role})
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

@router.post("/api/v1/endpoints/auth/reset-password/forgot-password/{email}", response_model=UserResponse)
async def reset_password(payload: str, email: str, db: Session = Depends(get_db)):
    
    db_user = crud_user.update_user(db=db, email=email, payload=payload)

    return db_user

@router.post("/api/v1/endpoints/auth/verify-account/")
async def account_verification(otp_token: str, otp: str):
    try:
        payload = decode_token(token=otp_token)

        if payload.get('otp') == otp:
            return {"Status": "success", 'message': "You loged in successfully"}
        else:
            raise exceptions.AuthorizationException("Otp is invalid.")
    except:
        raise exceptions.AuthenticationException("Server error")

    