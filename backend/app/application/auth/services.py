from fastapi import HTTPException, status
from app.domain.entities.models import User
from app.domain.repositories.contracts import UserRepository
from app.infrastructure.security.jwt import create_access_token, hash_password, verify_password
from app.schemas.dtos import Token, UserCreate


class AuthService:
    """Authentication use cases independent of transport and storage details."""

    def __init__(self, users: UserRepository):
        self.users = users

    async def register(self, payload: UserCreate) -> User:
        existing = await self.users.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
        return await self.users.create(User(email=payload.email, full_name=payload.full_name, role=payload.role, hashed_password=hash_password(payload.password)))

    async def login(self, email: str, password: str) -> Token:
        user = await self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return Token(access_token=create_access_token(user.email, user.role.value))
