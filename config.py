import logging.config
import os
import socket
import warnings
from enum import IntEnum

import requests
from pydantic import BaseModel, HttpUrl, FilePath, Field
from pydantic_settings import BaseSettings
from requests.exceptions import RequestsWarning


class SecurityWarning(RequestsWarning):
    """Custom security warning."""


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
    secret_token: str | None = Field(None, pattern="^[A-Za-z0-9_-]{1,256}$")
    debug: bool = False

    class Config:
        extra = "allow"
        env_file = os.environ.get('env_file', os.environ.get('ENV_FILE', '.env'))


settings = Settings()
assert settings.ngrok_token or settings.webhook, "\n\nEither a pre-configured webhook or Ngrok auth token is required"


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "TelegramAPI"
    LOG_FORMAT: str = "%(levelprefix)s %(message)s"
    LOG_LEVEL: str = "DEBUG" if settings.debug else "INFO"

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
    elif not settings.certificate:
        raise

if not any((settings.ngrok_token, settings.certificate)):
    logger.critical("Please make sure '%s' has a certificate backed by a trusted certificate authority (CA)",
                    settings.webhook)
    sample_openssl = 'openssl req -newkey rsa:2048 -sha256 -nodes -keyout PRIVATE.key -x509 -days 365 -out ' \
                     'PUBLIC.pem -subj "/C=US/ST=New York/L=Brooklyn/O=Example Brooklyn Company/CN=DOMAIN"'
    logger.critical("If not, please use a self-signed certificate by running\n'%s'", sample_openssl)

if not settings.secret_token:
    warnings.warn(
        "It is highly recommended to set a value for `secret_token`, "
        "as it will ensure the request comes from a webhook set by you.",
        SecurityWarning
    )

if 'ngrok' in settings.webhook.host.lower():
    logger.warning("Certificate is not required for an Ngrok reverse proxy, as it uses a trusted CA")
    settings.certificate = None
