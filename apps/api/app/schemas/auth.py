from pydantic import BaseModel, EmailStr, Field
from app.domain.entities.enums import UserRole
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.EMPLOYEE
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: UserRole
    model_config = {"from_attributes": True}
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
