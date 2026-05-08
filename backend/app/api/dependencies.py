from collections.abc import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.models import Role, User
from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.sqlalchemy_repositories import SqlAlchemyActionItemRepository, SqlAlchemyMeetingRepository, SqlAlchemyUserRepository
from app.infrastructure.security.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyUserRepository(session)


def get_meeting_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyMeetingRepository(session)


def get_action_repo(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyActionItemRepository(session)


async def get_current_user(token: str = Depends(oauth2_scheme), users=Depends(get_user_repo)) -> User:
    try:
        payload = decode_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    user = await users.get_by_email(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_roles(*roles: Role) -> Callable:
    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return checker
