from dataclasses import dataclass, asdict
from io import BytesIO


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
