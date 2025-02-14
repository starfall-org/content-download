from datetime import datetime

from hydrogram.enums import ChatType
from hydrogram.types import InlineKeyboardMarkup, Message
from pydantic import BaseModel


class Atributes(BaseModel):
    url: str
    button: InlineKeyboardMarkup
    caption: str

    class Config:
        arbitrary_types_allowed = True


class LinkInfo(BaseModel):
    is_video: bool
    url: str
    title: str | None = None


class Links(BaseModel):
    standalone: bool
    content: list[LinkInfo] | LinkInfo

    class Config:
        arbitrary_types_allowed = True


class APIResult(BaseModel):
    result: Links
    button: InlineKeyboardMarkup
    caption: str

    class Config:
        arbitrary_types_allowed = True


class ChatArgs(BaseModel):
    message: Message
    is_admin: bool
    is_banned: bool
    can_reply: bool
    is_channel: bool = False
    is_group: bool = False
    is_supergroup: bool = False

    def get_administrators(self):
        return [7642104102]

    class Config:
        arbitrary_types_allowed = True


class LogMessage(BaseModel):
    action: str
    date: datetime = datetime.now()
    user: str
    message: Message

    class Config:
        arbitrary_types_allowed = True
