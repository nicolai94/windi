from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, func
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.config import settings
from src.storage.models.base import Base
from src.storage.models.mixins.id_int_pk import IdIntPkMixin


if TYPE_CHECKING:
    from src.storage.models.chat import Chat
    from src.storage.models.user import User


class Message(IdIntPkMixin, Base):
    text: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=func.timezone(settings.default_timezone, func.now())
    )
    is_read: Mapped[bool] = Column(Boolean, default=False)

    chat_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("chats.id", ondelete="CASCADE"),
        nullable=False,
    )

    sender_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    sender: Mapped["User"] = relationship("User")
