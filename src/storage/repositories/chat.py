from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.schemas.chat import ChatCreateInput
from src.storage import Chat
from src.storage.models.message import Message

from src.storage.repositories.base import BaseRepository


class ChatRepository(BaseRepository[Chat]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Chat)

    async def get_history(
        self, chat_id: int, limit: int = 50, offset: int = 0
    ) -> Tuple:
        chat_stmt = select(self.model).where(self.model.id == chat_id)
        chat_result = await self.session.execute(chat_stmt)
        chat = chat_result.scalars().first()

        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        messages = result.scalars().all()

        return chat, messages

    async def create_chat(self, data: ChatCreateInput):
        chat = Chat(**data.model_dump(exclude_none=True))
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)

        return chat

    async def get_chat_by_id(self, chat_id: int) -> Chat | None:
        stmt = select(self.model).where(self.model.id == chat_id)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
