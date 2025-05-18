import pytest
from sqlalchemy import select
from httpx import AsyncClient
from src.storage import User
from tests.fixtures.db import TestingSessionLocal


@pytest.mark.asyncio
async def test_register_and_login(async_client: AsyncClient):
    register_data = {"name": "Test", "email": "test@mail.com", "password": "pass"}
    register_response = await async_client.post(
        "/api/auth/register",
        json=register_data,
    )
    assert register_response.status_code == 200

    login_form = {"username": "test@mail.com", "password": "pass"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    login_response = await async_client.post(
        "api/auth/login", data=login_form, headers=headers
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    async with TestingSessionLocal() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        assert len(users) == 1
        assert users[0].email == register_data["email"]
        assert users[0].name == register_data["name"]
