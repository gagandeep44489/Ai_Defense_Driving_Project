"""User request and response schemas."""
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    """Payload used to create a user."""
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=12, max_length=128)
    roles: list[str] = ['analyst']

class UserRead(BaseModel):
    """Safe user representation returned by APIs."""
    id: int
    email: EmailStr
    full_name: str
    roles: list[str]
    is_active: bool
