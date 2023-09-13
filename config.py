import logging.config
import os
import socket
from enum import IntEnum

import requests
from pydantic import BaseModel, HttpUrl, FilePath
from pydantic_settings import BaseSettings


class AllowedPorts(IntEnum):
    tcp: int = 88
    http: int = 80
    https: int = 443
    openssl: int = 8443


class Settings(BaseSettings):
    """Env configuration.

    References:
        https://docs.pydantic.dev/2.3/migration/#required-optional-and-nullable-fields
    """

    bot_token: str

    ngrok_token: str | None = None
    webhook: HttpUrl | None = None
    endpoint: str = "/telegram-webhook"

    host: str = socket.gethostbyname("localhost")
    port: AllowedPorts = 8443
    certificate: FilePath | None = None

    class Config:
        extra = "allow"
        env_file = os.environ.get('env_file', os.environ.get('ENV_FILE', '.env'))


settings = Settings()
assert settings.ngrok_token or settings.webhook, "\n\nEither a pre-configured webhook or Ngrok auth token is required"


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

if settings.webhook and settings.webhook.scheme == "http":
    raise ValueError(
        "\n\nPre-configured webhook should be able to handle TLS1.2(+) HTTPS-traffic"
    )

try:
    requests.get(url=settings.webhook, timeout=1)
except requests.exceptions.SSLError as error:
    if "self-signed certificate" in error.__str__() and not settings.certificate:
        raise ValueError(
            "\n\n'CERTIFICATE' is required for webhooks backed by a self-signed certificate for verification"
        )
    else:
        raise

if not any((settings.ngrok_token, settings.certificate)):
    logger.critical("Please make sure '%s' has a certificate backed by a trusted certificate authority (CA)",
                    settings.webhook)
    sample_openssl = 'openssl req -newkey rsa:2048 -sha256 -nodes -keyout PRIVATE.key -x509 -days 365 -out ' \
                     'PUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=DOMAIN"'
    logger.critical("If not, please use a self-signed certificate by running\n'%s'", sample_openssl)
