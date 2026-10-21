from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import user
from app.crud import crud_user
from app.schemas import token
from app.core.database import get_db
from app.core import security
from jose import jwt, JWTError
from app.core.config import settings
from app.core import exceptions
from app.api import deps
from app.core import redis
from app.services import email_service
from app.models import user as User
import sqlalchemy as sq

router = APIRouter()

@router.post("/api/v1/endpoints/auth/sign-up", response_model=user.UserResponse)
async def register(user: user.UserRequest, background_taks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        db_user = crud_user.get_user(db=db, email=user.email)

        if db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

        new_user = crud_user.create_user(db=db, user=user)

        background_taks.add_task(
            email_service.send_email,
            email=user.email,
            username=user.name,
        )
        
        return new_user
    except:
        db.rollback()
        raise exceptions.AuthenticationException("Server error.")

@router.post("/api/v1/endpoints/auth/login")
async def logs_in(background_taks: BackgroundTasks, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        db_user = security.authentication_user(db=db, email=form.username, password=form.password)

        if not db_user:             
            raise exceptions.AuthenticationException("you did not registered yourself yet.")

        if deps.role_checker(role=db_user.role):
            raise exceptions.AuthenticationException("Sorry you can't log in.")

        otp = email_service.generate_otp()

        background_taks.add_task(
            email_service.send_otp_email,
            email=db_user.email,
            username=db_user.name,
            otp=otp,
        )
        
        
        if not otp:
            raise exceptions.AuthenticationException("Invalid otp.")

        otp_token = security.create_otp_token(data={'sub': db_user.email, 'otp': otp, "role": db_user.role})

        return {"status": "success", "otp_token": otp_token}
    except:
        db.rollback()
        raise 

@router.post("/api/v1/endpoints/auth/refresh_token/", response_model=token.RefreshTokenResponse)
def new_access_token(refresh_token: str):
    try:
        payload = deps.decode_token(token=refresh_token)

        if payload.get('type') != 'refresh':
            raise exceptions.AuthenticationException("Invalid token type. Expected a refresh token.") 

        if not payload.get("sub"):
            raise exceptions.AuthenticationException("Invalid token payload. Missing 'email' claim.")

        new_access_token = security.create_access_token(data={'sub': payload.get("sub"), "role": payload.get("role")})
        return {"access_token": new_access_token, "token_type": "Bearer"}
    except JWTError:
        raise exceptions.AuthenticationException("Invalid refresh token.")

@router.post("/api/v1/endpoints/auth/logout")
def logout(refresh_token: str):
    payload = deps.decode_token(token=refresh_token)

    if not payload.get("jti"):
        raise exceptions.AuthenticationException("Invalid request for logout")

    redis.revoke_token(jti=payload.get("jti"), expires_in=settings.EXPIRY_TIME)

    return {'status': "success", "message": "Logout Successfully."}

@router.post("/api/v1/endpoints/auth/reset-password/forgot-password/{email}", response_model=user.UserResponse)
async def reset_password(payload: str, email: str, db: Session = Depends(get_db)):
    
    db_user = crud_user.update_user(db=db, email=email, payload=payload)

    return db_user

@router.post("/api/v1/endpoints/auth/verify-account", response_model=token.Token)
async def account_verification(otp_payload: token.OtpVerification, db: Session = Depends(get_db)):
    try:
        payload = deps.decode_token(token=otp_payload.otp_token)

        db_user = crud_user.get_user(db=db, email=payload.get("sub"))

        if not db_user:
            raise exceptions.AuthenticationException("You did not registered yet.")

        if payload.get('otp') != otp_payload.otp:
            raise exceptions.AuthorizationException("Otp is invalid.")
        else:
            access_token = security.create_access_token(data={'sub': payload.get("sub"), 'role': payload.get("role")})
            refresh_token = security.create_refresh_token(data={'sub': payload.get("sub"), 'role': payload.get("role")})
            
        if db_user.is_verified:
            stmt = sq.update(User.User).where(User.User.email == payload.get("sub")).values(is_verified=True)
            db.execute(stmt)
            db.commit()
        
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except:
        raise
    