from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    webhook: HttpUrl
    ngrok_token: str | None
    host: str = "localhost"
    port: int = 8443

    class Config:
        extra = "allow"
        env_file = ".env"


settings = Settings()
