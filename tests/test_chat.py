import pytest
from httpx import AsyncClient
from sqlalchemy import select

from src.storage import Chat, Message
from src.storage.models.enums import ChatType
from tests.fixtures.db import TestingSessionLocal

pytestmark = pytest.mark.asyncio


async def test_message_history(chat: Chat, message: Message, async_client: AsyncClient):
    response = await async_client.get(f"/api/chat/{chat.id}")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == chat.name
    assert data["messages"][0]["id"] == message.id
    assert data["messages"][0]["text"] == message.text


async def test_create_chat(async_client: AsyncClient):
    params = {
        "name": "test",
        "chatType": ChatType.PRIVATE.value,
    }
    response = await async_client.post("/api/chat/", json=params)
    print(f"{response.json()=}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == params["name"]
    assert data["chatType"] == params["chatType"]

    async with TestingSessionLocal() as session:
        stmt = select(Chat)
        result = await session.execute(stmt)
        chats = result.scalars().all()
        assert len(chats) == 1
