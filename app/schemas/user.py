from pydantic import BaseModel, ConfigDict, Field

class UserRequest(BaseModel):
    name: str
    email: str
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = None

class UserResponse(BaseModel):
    name: str
    email: str
    phone: str | None

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    phone: str | None = None