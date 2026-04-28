from dataclasses import asdict, dataclass
from io import BytesIO


@dataclass
class CommonLink:
    url: str | BytesIO
    type: str

    def to_dict(self):
        return asdict(self)


@dataclass
class CommonLinks:
    links: list[CommonLink]
    title: str
    platform: str
    original: str

    def to_dict(self):
        return asdict(self)


@dataclass
class YoutubeLink:
    url: str | BytesIO
    quality: str
    extension: str
    type: str

    def to_dict(self):
        return asdict(self)


@dataclass
class YoutubeLinks:
    video: YoutubeLink
    video_no_audio: YoutubeLink
    audio: YoutubeLink
    title: str
    thumbnail: str
    original: str

    def to_dict(self):
        return asdict(self)
