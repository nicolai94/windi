from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from src.utils.case_converter import to_camel

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class CommonConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class BaseDBConfig(BaseSchema):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 5

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class DatabaseConfig(BaseDBConfig): ...


class DatabaseTestConfig(BaseDBConfig): ...


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    auth: str = "/auth"
    chat: str = "/chat"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="allow",
    )
    api: ApiPrefix = ApiPrefix()
    common: CommonConfig
    db: DatabaseConfig
    db_test: DatabaseTestConfig
    version: str = "0.1.0"
    default_timezone: str = "Europe/Moscow"
    run: RunConfig = RunConfig()


settings = Settings()  # type: ignore
