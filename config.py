import logging.config
import os
import socket

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """

    References:
        https://docs.pydantic.dev/2.3/migration/#required-optional-and-nullable-fields
    """

    bot_token: str
    ngrok_token: str | None

    host: str = socket.gethostbyname("localhost")
    port: int = 8443

    class Config:
        extra = "allow"
        env_file = os.environ.get('env_file', os.environ.get('ENV_FILE', '.env'))


settings = Settings()


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "TelegramAPI"
    LOG_FORMAT: str = "%(levelprefix)s %(message)s"
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


logging.config.dictConfig(LogConfig().model_dump())
logger = logging.getLogger("TelegramAPI")
