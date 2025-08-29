from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).parent.parent.parent

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    endpoint: str = "/endpoint"
    tasks: str = "/tasks"
    comments: str = "/comments"
    calendar: str = "/calendar"
    meetings: str = "/meetings"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

class BaseURL(BaseModel):
    user_url: str = "http://localhost:8000"
    api: ApiPrefix = ApiPrefix()


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str


class DataBase(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int


class GunicornConfig(BaseModel):
    host: str
    port: int
    workers: int
    timeout: int

class JWTToken(BaseModel):
    algorithm: str = "RS256"
    public_key: Path = BASE_PATH / "certs" / "jwt-public.pem"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_PATH / ".template.env",
            BASE_PATH / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    gunicorn: GunicornConfig
    db: DataBase
    logging: LoggingConfig
    base_url: BaseURL = BaseURL()
    api_key: str = "qwerty"
    jwt_token: JWTToken = JWTToken()


settings = Settings()
