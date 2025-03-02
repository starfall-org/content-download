from pydantic import BaseModel


class APIResult(BaseModel):
    is_video: bool
    url: str
    title: str | None = None


class APIResultGroup(BaseModel):
    standalone: bool
    content: list[APIResult] | APIResult

    class Config:
        arbitrary_types_allowed = True
