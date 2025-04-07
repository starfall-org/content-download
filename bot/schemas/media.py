import io
from dataclasses import dataclass


@dataclass
class Media:
    data: io.BytesIO
    mime_type: str
