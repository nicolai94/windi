from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.storage.models.message import Message

from src.storage.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Message)

    async def get_message_by_id(self, message_id: int) -> Message | None:
        stmt = select(self.model).where(self.model.id == message_id)
        result = await self.session.execute(stmt)

        return result.scalars().first()

    async def create_message(self, chat_id: int, sender_id: int, text: str):
        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text,
        )
        self.session.add(message)

        try:
            await self.session.commit()
            await self.session.refresh(message)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

        return message

    async def update_data(
        self, message_id: int, chat_id: int, user_id: int, data: dict
    ) -> None:
        message = (
            update(self.model)
            .where(
                self.model.chat_id == chat_id,
                self.model.id <= message_id,
                self.model.is_read.is_(False),
                self.model.sender_id != user_id,
            )
            .values(**data)
        )

        try:
            await self.session.execute(message)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise
