from pydantic import BaseModel
from app.models.user import RoleType

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str