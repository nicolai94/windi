import json

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket, HTTPException
from starlette import status
from starlette.websockets import WebSocketDisconnect

from src.api.schemas.chat import (
    ChatCreateInput,
    ChatCreateOutput,
    ChatHistoryOutput,
    ChatMessageOutput,
)
from src.storage.models.enums import ChatType
from src.storage.repositories.chat import ChatRepository
from src.storage.repositories.group import GroupRepository
from src.storage.repositories.message import MessageRepository
from src.storage.repositories.user import UserRepository
from src.utils.connection_manager import manager


class ChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_history(
        self, chat_id: int, limit: int = 50, offset: int = 0
    ) -> ChatHistoryOutput:
        chat_repo = ChatRepository(self.session)
        chat, messages = await chat_repo.get_history(chat_id, limit, offset)

        return ChatHistoryOutput(
            messages=[
                ChatMessageOutput(
                    id=message.id,
                    sender_id=message.sender_id,
                    text=message.text,
                    is_read=message.is_read,
                    timestamp=message.timestamp,
                )
                for message in messages
            ],
            name=chat.name,
        )

    async def create_chat(self, data: ChatCreateInput) -> ChatCreateOutput:
        chat_repo = ChatRepository(self.session)
        chat = await chat_repo.create_chat(data)

        if data.chat_type == ChatType.GROUP:
            user_repo = UserRepository(self.session)
            user = await user_repo.get_user_by_id(data.user_id)
            members = await user_repo.get_users_by_ids(data.members)

            if not user:
                logger.error("User not found")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

            group_repo = GroupRepository(self.session)
            await group_repo.create_group(data.group_name, user, members)

        return chat

    async def websocket_chat(
        self, websocket: WebSocket, chat_id: int, user_id: int
    ) -> None:
        await manager.connect(chat_id, user_id, websocket)

        try:
            message_repo = MessageRepository(self.session)
            chat_repo = ChatRepository(self.session)
            chat = await chat_repo.get_chat_by_id(chat_id)

            if not chat:
                await websocket.send_text(json.dumps({"error": "Chat not found"}))
                logger.error("Chat not found")
                await websocket.close()
                return

            while True:
                raw_data = await websocket.receive_text()
                try:
                    data = json.loads(raw_data)
                except json.JSONDecodeError:
                    await websocket.send_text(
                        json.dumps({"error": "Invalid JSON format"})
                    )
                    logger.error("Invalid JSON format")
                    continue

                if text := data.get("text"):
                    if data.get("messageId"):
                        exists = await message_repo.get_message_by_id(data["messageId"])
                        if exists:
                            continue

                    msg = await message_repo.create_message(chat_id, user_id, text)

                    await manager.broadcast(
                        chat_id,
                        json.dumps(
                            {
                                "id": msg.id,
                                "chatId": chat_id,
                                "senderId": user_id,
                                "text": msg.text,
                                "timestamp": str(msg.timestamp),
                                "isRead": msg.is_read,
                            }
                        ),
                    )
                elif read_id := data.get("readId"):
                    msg_id = read_id
                    message = await message_repo.get_message_by_id(msg_id)
                    if not message or message.is_read:
                        continue

                    await message_repo.update_data(
                        msg_id, chat_id, user_id, {"is_read": True}
                    )

                    await manager.broadcast(
                        chat_id, json.dumps({"read_update": message.id})
                    )

        except WebSocketDisconnect:
            manager.disconnect(chat_id, user_id)
