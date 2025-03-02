from hydrogram.types import InlineKeyboardMarkup, Message
from pydantic import BaseModel
from .api_models import APIResultGroup


class FilteredMessageAtributes(BaseModel):
    url: str
    button: InlineKeyboardMarkup
    caption: str

    class Config:
        arbitrary_types_allowed = True


class PreResponseAtributes(BaseModel):
    result: APIResultGroup
    button: InlineKeyboardMarkup
    caption: str

    class Config:
        arbitrary_types_allowed = True


class ParsedChatArguments(BaseModel):
    message: Message
    is_admin: bool = False
    is_banned: bool = False
    can_reply: bool = True
    is_channel: bool = False
    is_group: bool = False
    is_supergroup: bool = False

    def get_administrators(self):
        return [7642104102]

    class Config:
        arbitrary_types_allowed = True
