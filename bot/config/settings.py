import os
from dataclasses import dataclass


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    bot_token: str
    database_url: str
    content_api: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            bot_token=_require_env("BOT_TOKEN"),
            database_url=_require_env("DATABASE_URL"),
            content_api=_require_env("CONTENT_API").rstrip("/"),
        )


settings = Settings.from_env()

BOT_TOKEN = settings.bot_token
DATABASE_URL = settings.database_url
CONTENT_API = settings.content_api
