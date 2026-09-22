from pydantic import BaseModel

class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    role: str

class UserResponse(BaseModel):
    name: str
    email: str
    phone: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None