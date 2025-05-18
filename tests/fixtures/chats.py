import pytest_asyncio

from src.storage import Chat
from src.storage.models.enums import ChatType
from tests.fixtures.db import TestingSessionLocal


@pytest_asyncio.fixture
async def chat() -> Chat:
    async with TestingSessionLocal() as session:
        chat = Chat(name="test", chat_type=ChatType.PRIVATE)
        session.add(chat)
        await session.commit()
        await session.refresh(chat)

    return chat
