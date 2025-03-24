from dataclasses import dataclass
from typing import Literal


@dataclass
class ResponseItem:
    url: str
    mediatype: Literal["image", "video", "audio"]
    title: str | None = None


@dataclass
class ResponseGroup:
    is_list: bool
    content: list[ResponseItem] | ResponseItem
