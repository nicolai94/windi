# Windi Messenger

## 🚀 Описание
Проект — асинхронный мессенджер с поддержкой:
- WebSocket чатов (личные и групповые)
- Истории сообщений
- JWT авторизации по стандарту OAuth2
- PostgreSQL через async SQLAlchemy
- Docker-контейнеризация

---

## 🐳 Запуск через Docker

### 1. Собрать и запустить:
создать файл .env из .env_template
```bash
docker-compose up --build
```

### 2. Сервер будет доступен на:
- `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

---

## 🔐 Аутентификация (JWT + OAuth2)

### Регистрация
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "Test",
  "email": "user@example.com",
  "password": "secure"
}
```

### Логин (OAuth2PasswordRequestForm)
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure
```

### Результат:
```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Используется в заголовке:
```http
Authorization: Bearer <access_token>
```

---

## 💬 API: Чаты

### Создание чата
```http
POST /api/chat/
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "test-chat",
  "chat_type": "PRIVATE",
  "user_id": 2
}
```

### Получение истории
```http
GET /api/chat/1?limit=50&offset=0
Authorization: Bearer <token>
```

Ответ:
```json
{
  "name": "test-chat",
  "messages": [
    {
      "id": 1,
      "text": "Привет",
      "timestamp": "2025-05-15T08:00:00Z",
      "sender_id": 1,
      "is_read": true
    }
  ]
}
```

---

## 🔄 WebSocket подключение
```js
const socket = new WebSocket("ws://localhost:8000/api/chat/1/1")

socket.send(JSON.stringify({
  text: "Привет!",
  message_id: "int"
}))

socket.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  console.log("Получено сообщение:", msg);
}
```
---

## ✅ Тесты
```bash
docker compose exec backend poetry run pytest -vv
```

---

## 📂 Структура
```
src/
├── api/                # FastAPI endpoints
├── core/               # Настройки, security, конфиг
├── services/           # Сервисы
├── storage/            # SQLAlchemy модели и репозитории
├── utils/              # Вспомогательные функции
├── main.py             # Точка входа
tests/                  # Тесты
```

---