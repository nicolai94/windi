from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api import router as api_router
from src.core.config import settings
from src.storage.models.db_helper import db_connector


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_connector.dispose()


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app = FastAPI(
    lifespan=lifespan
)

register_middleware(app)
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
