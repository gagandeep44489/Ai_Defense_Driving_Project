from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.models import User
from app.infrastructure.database.session import get_db
from app.infrastructure.security.auth import decode_token

bearer = HTTPBearer(auto_error=False)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer), db: AsyncSession = Depends(get_db)) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try: payload = decode_token(credentials.credentials)
    except ValueError as exc: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    result = await db.execute(select(User).where(User.email == payload.get("sub"), User.is_active.is_(True)))
    user = result.scalar_one_or_none()
    if user is None: raise HTTPException(status_code=401, detail="User not found")
    return user

def require_roles(*roles: str):
    async def checker(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker
