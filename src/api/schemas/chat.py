from datetime import datetime

from src.core.config import BaseSchema
from src.storage.models.enums import ChatType


class ChatCreateInput(BaseSchema):
    name: str
    chat_type: ChatType = ChatType.PRIVATE
    group_name: str | None = None
    user_id: int | None = None
    member_ids: list[int] | None = None


class ChatCreateOutput(BaseSchema):
    id: int
    name: str
    chat_type: ChatType = ChatType.PRIVATE


class ChatMessageOutput(BaseSchema):
    id: int
    text: str
    timestamp: datetime
    sender_id: int
    is_read: bool


class ChatHistoryOutput(BaseSchema):
    name: str
    messages: list[ChatMessageOutput]
