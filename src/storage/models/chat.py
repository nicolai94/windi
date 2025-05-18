from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.models.base import Base
from src.storage.models.enums import ChatType
from src.storage.models.mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from src.storage.models.message import Message


class Chat(IdIntPkMixin, Base):
    name: Mapped[str]
    chat_type: Mapped[ChatType] = mapped_column(
        Enum(ChatType), server_default=ChatType.PRIVATE
    )

    messages: Mapped["Message"] = relationship(back_populates="chat")
