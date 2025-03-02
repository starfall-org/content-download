from hydrogram.types import InputMediaPhoto, InputMediaVideo

from helpers.io_tool import url_to_io
from models.api_models import APIResult


def parse_media_group(
    media: list[APIResult],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return [
        InputMediaVideo(link.url) if link.is_video else InputMediaPhoto(link.url)
        for link in media
    ]


async def convert_to_io(media: list[APIResult]) -> list[APIResult]:
    return [APIResult(link.is_video, await url_to_io(link.url)) for link in media]
