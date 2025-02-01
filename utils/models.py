from pydantic import BaseModel
from hydrogram.types import InlineKeyboardMarkup


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
