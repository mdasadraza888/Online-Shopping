from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserRequest, UserResponse
from app.api.deps import get_current_user
from app.models.user import User


user_route = APIRouter()

@user_route.get("/me", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

