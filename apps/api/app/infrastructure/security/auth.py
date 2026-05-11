from datetime import UTC, datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(password: str, hashed: str) -> bool: return pwd_context.verify(password, hashed)

def create_access_token(subject: str, role: str) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "role": role, "exp": expire}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> dict:
    settings = get_settings()
    try: return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc: raise ValueError("Invalid authentication token") from exc
