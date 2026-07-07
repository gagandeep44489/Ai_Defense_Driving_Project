"""Application service for user lifecycle commands."""
from sovereignai.core.security import hash_password
from sovereignai.users.models import UserModel
from sovereignai.users.repository import UserRepository
from sovereignai.users.schemas import UserCreate

class UserService:
    """Coordinates user use cases without leaking persistence details."""
    def __init__(self, repository: UserRepository) -> None: self.repository = repository
    def create_user(self, payload: UserCreate) -> UserModel:
        """Create a user and enforce unique email addresses."""
        if self.repository.get_by_email(payload.email):
            raise ValueError('user already exists')
        return self.repository.add(UserModel(email=payload.email, full_name=payload.full_name, password_hash=hash_password(payload.password), roles=','.join(payload.roles)))
