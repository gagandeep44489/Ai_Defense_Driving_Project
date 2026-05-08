import pytest
from app.application.auth.services import AuthService
from app.domain.entities.models import User
from app.schemas.dtos import UserCreate


class FakeUsers:
    def __init__(self):
        self.users = {}
        self.next_id = 1

    async def get_by_email(self, email: str):
        return self.users.get(email)

    async def create(self, user: User):
        user.id = self.next_id
        self.next_id += 1
        self.users[user.email] = user
        return user


@pytest.mark.asyncio
async def test_register_and_login_returns_token():
    repo = FakeUsers()
    service = AuthService(repo)

    user = await service.register(UserCreate(email="admin@example.com", full_name="Admin User", password="strong-password", role="admin"))
    token = await service.login("admin@example.com", "strong-password")

    assert user.email == "admin@example.com"
    assert token.access_token
