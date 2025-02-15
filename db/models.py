from datetime import datetime
from sqlmodel import SQLModel, Field


class PresetContent(SQLModel, table=True):
    __tablename__ = "contentdownload_presets"
    id: int = Field(primary_key=True)
    name: str
    content: str


class Chat(SQLModel, table=True):
    __tablename__ = "contentdownload_chats"
    id: int = Field(primary_key=True)
    username: str | None = Field(default=None)
    title: str
    is_user: bool = Field(default=False)
    is_channel: bool = Field(default=False)
    is_group: bool = Field(default=False)
    is_supergroup: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    is_banned: bool = Field(default=False)
    can_reply: bool = Field(default=True)
    last_active: datetime = Field(default_factory=datetime.now)
