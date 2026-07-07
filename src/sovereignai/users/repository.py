"""Repository pattern implementation for users."""
from sqlalchemy import select
from sqlalchemy.orm import Session
from sovereignai.users.models import UserModel

class UserRepository:
    """Encapsulates user database queries."""
    def __init__(self, session: Session) -> None: self.session = session
    def get_by_email(self, email: str) -> UserModel | None:
        """Return a user by email if present."""
        return self.session.scalar(select(UserModel).where(UserModel.email == email))
    def add(self, user: UserModel) -> UserModel:
        """Persist a new user model."""
        self.session.add(user); self.session.flush(); return user
