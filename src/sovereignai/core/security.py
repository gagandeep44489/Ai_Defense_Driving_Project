"""Security primitives for password hashing, JWTs, and sanitisation."""
from datetime import UTC, datetime, timedelta
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from sovereignai.config.settings import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a password hash."""
    return pwd_context.verify(password, password_hash)

def create_access_token(subject: str, roles: list[str], expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT access token."""
    settings = get_settings(); expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.access_token_minutes))
    payload: dict[str, Any] = {'sub': subject, 'roles': roles, 'exp': expire, 'type': 'access'}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(subject: str) -> str:
    """Create a signed JWT refresh token."""
    settings = get_settings(); expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_days)
    return jwt.encode({'sub': subject, 'exp': expire, 'type': 'refresh'}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
