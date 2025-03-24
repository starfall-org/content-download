from dataclasses import dataclass

from hydrogram.types import InlineKeyboardMarkup, Message

from .api import ResponseGroup


@dataclass
class ParsedAtributes:
    url: str
    button: InlineKeyboardMarkup
    caption: str


@dataclass
class ResponseUtility:
    result: ResponseGroup
    button: InlineKeyboardMarkup
    caption: str


@dataclass
class ParsedChatArguments:
    message: Message
    is_admin: bool = False
    is_banned: bool = False
    can_reply: bool = True
    is_channel: bool = False
    is_group: bool = False
    is_supergroup: bool = False

    def get_administrators(self):
        return [7642104102]
