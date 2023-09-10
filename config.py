import logging.config
import socket

from pydantic import HttpUrl, BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    webhook: HttpUrl
    ngrok_token: str | None
    host: str = socket.gethostbyname("localhost")
    port: int

    class Config:
        extra = "allow"
        env_file = ".env"


settings = Settings()


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "TelegramAPI"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


logging.config.dictConfig(LogConfig().dict())
logger = logging.getLogger("TelegramAPI")
