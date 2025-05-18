from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, dict[int, WebSocket]] = {}

    async def connect(self, chat_id: int, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(chat_id, {})[user_id] = websocket

    def disconnect(self, chat_id: int, user_id: int):
        self.active_connections[chat_id].pop(user_id, None)

    async def broadcast(self, chat_id: int, message: str):
        for websocket in self.active_connections.get(chat_id, {}).values():
            await websocket.send_text(message)


manager = ConnectionManager()
