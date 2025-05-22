from dataclasses import dataclass

from hydrogram.types import InlineKeyboardMarkup, Message

from .api import ResponseGroup
from .common_link import CommonLinks
from .youtube_link import YoutubeLinks


@dataclass
class ParsedAtributes:
    url: str
    button: InlineKeyboardMarkup
    caption: str


@dataclass
class ResponseUtility:
    result: YoutubeLinks | CommonLinks
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
