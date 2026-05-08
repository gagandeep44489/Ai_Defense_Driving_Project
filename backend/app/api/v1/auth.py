from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import get_user_repo
from app.application.auth.services import AuthService
from app.schemas.dtos import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: UserCreate, users=Depends(get_user_repo)):
    return await AuthService(users).register(payload)


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), users=Depends(get_user_repo)):
    return await AuthService(users).login(form.username, form.password)
