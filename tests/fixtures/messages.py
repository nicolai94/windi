import pytest_asyncio

from src.storage import Chat, Message, User
from tests.fixtures.db import TestingSessionLocal


@pytest_asyncio.fixture
async def message(chat: Chat, user: User) -> Message:
    async with TestingSessionLocal() as session:
        message = Message(
            text="test",
            chat_id=chat.id,
            sender_id=user.id,
            is_read=False,
        )
        session.add(message)
        await session.commit()
        await session.refresh(message)

    return message
