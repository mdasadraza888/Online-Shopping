from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserRequest, UserResponse
from app.crud.crud_user import get_user, create_user
from app.schemas.token import Token
from app.core.database import get_db
from app.core.security import create_access_token, verify_hashed_password, authentication_user

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

@router.post("/login", response_model=Token)
def login_to_access_token(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        db_user = authentication_user(db=db, email=form.username, password=form.password)

        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

        token = create_access_token(data={'sub': db_user.name, 'email': db_user.email, 'role': db_user.role.value})
        return {"access_token": token, "token_type": "bearer"}
    except:
        db.rollback()
        raise