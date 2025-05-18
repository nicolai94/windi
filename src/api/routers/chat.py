from fastapi import APIRouter
from starlette.websockets import WebSocket

from src.api.schemas.chat import ChatCreateInput, ChatCreateOutput, ChatHistoryOutput
from src.services.chat import ChatService
from src.storage.models.db_helper import Session

router = APIRouter()


@router.get("/{chat_id}", response_model=ChatHistoryOutput)
async def history(chat_id: int, session: Session, limit: int = 50, offset: int = 0):
    chat_service = ChatService(session)

    return await chat_service.get_history(chat_id, limit, offset)


@router.post("/", response_model=ChatCreateOutput)
async def create_chat(data: ChatCreateInput, session: Session) -> ChatCreateOutput:
    chat_service = ChatService(session)

    return await chat_service.create_chat(data)


@router.websocket("/{chat_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket, chat_id: int, user_id: int, session: Session
):
    chat_service = ChatService(session)
    await chat_service.websocket_chat(websocket, chat_id, user_id)
