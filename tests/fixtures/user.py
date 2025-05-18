import pytest_asyncio

from src.storage import User
from tests.fixtures.db import TestingSessionLocal


@pytest_asyncio.fixture
async def user() -> User:
    async with TestingSessionLocal() as session:
        user = User(name="test", email="test", password="test")
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user
