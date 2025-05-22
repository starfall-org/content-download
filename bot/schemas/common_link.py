from dataclasses import dataclass, asdict
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
