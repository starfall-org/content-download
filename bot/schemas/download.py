from dataclasses import asdict, dataclass, field
from io import BytesIO
from typing import Any


@dataclass
class CommonLink:
    """A single media item from the canonical Content API response."""

    url: str | BytesIO
    type: str  # video, image, audio, document, hls
    quality: str | None = None
    extension: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CommonLinks:
    """Canonical Content API success response, shared by every platform."""

    success: bool
    platform: str
    original_url: str
    resolved_url: str | None = None
    title: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    media: list[CommonLink] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
