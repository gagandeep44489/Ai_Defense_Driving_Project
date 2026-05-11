from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models import User
from app.infrastructure.database.session import get_db
from app.infrastructure.security.auth import create_access_token, hash_password, verify_password
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead
router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register", response_model=Token, status_code=201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none(): raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password), role=payload.role)
    db.add(user); await db.commit(); await db.refresh(user)
    return Token(access_token=create_access_token(user.email, user.role.value), user=UserRead.model_validate(user))
@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> Token:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=create_access_token(user.email, user.role.value), user=UserRead.model_validate(user))
