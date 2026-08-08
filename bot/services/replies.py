from aiohttp import ClientSession, ClientTimeout
from hydrogram.enums import ChatAction
from hydrogram.types import Message

from bot.schemas.download import CommonLink, CommonLinks
from bot.schemas.telegram import ResponseUtility
from bot.services.media_converter import convert_to_io

MediaLink = CommonLink
AUDIO_TITLE = "music"
AUDIO_PERFORMER = "music.mp3"


def _links(result: CommonLinks) -> list[MediaLink]:
    return result.media


def _split_media(items: list[MediaLink]) -> tuple[list[MediaLink], list[MediaLink]]:
    audio = [item for item in items if item.type.lower() == "audio"]
    visual = [item for item in items if item.type.lower() != "audio"]
    return visual, audio


def _same_type_index(items: list[MediaLink], index: int) -> int:
    media_type = items[index].type
    return sum(item.type == media_type for item in items[: index + 1]) - 1


def _chat_action(media_type: str) -> ChatAction:
    media_type = media_type.lower()
    if media_type in {"video", "hls"}:
        return ChatAction.UPLOAD_VIDEO
    if media_type == "audio":
        return ChatAction.UPLOAD_AUDIO
    if media_type == "document":
        return ChatAction.UPLOAD_DOCUMENT
    return ChatAction.UPLOAD_PHOTO


async def _converted_links(data: ResponseUtility, media_type: str) -> list[MediaLink]:
    converted = await convert_to_io(data.result)
    return [item for item in _links(converted) if item.type.lower() == media_type.lower()]


async def _send_visual(
    message: Message,
    item: MediaLink,
    caption: str | None = None,
    reply_markup=None,
) -> None:
    media_type = item.type.lower()
    await message.reply_chat_action(_chat_action(media_type))
    kwargs = {"reply_markup": reply_markup}
    if caption:
        kwargs["caption"] = caption

    if media_type in {"video", "hls"}:
        await message.reply_video(item.url, **kwargs)
    elif media_type == "image":
        await message.reply_photo(item.url, **kwargs)
    elif media_type == "document":
        await message.reply_document(item.url, **kwargs)
    else:
        raise ValueError(f"Unsupported media type: {item.type}")


async def _send_visual_with_fallback(
    message: Message,
    item: MediaLink,
    data: ResponseUtility,
    caption: str | None = None,
    reply_markup=None,
    fallback_index: int = 0,
) -> None:
    try:
        await _send_visual(message, item, caption=caption, reply_markup=reply_markup)
        return
    except Exception:
        fallback_links = await _converted_links(data, item.type)

    if fallback_index < len(fallback_links):
        await _send_visual(
            message,
            fallback_links[fallback_index],
            caption=caption,
            reply_markup=reply_markup,
        )


async def _url_is_reachable(url: object) -> bool:
    if not isinstance(url, str):
        return True
    try:
        async with ClientSession() as session:
            async with session.head(
                url,
                allow_redirects=True,
                timeout=ClientTimeout(total=5),
            ) as response:
                return response.status < 400
    except Exception:
        return False


async def _audio_url(data: ResponseUtility, audio: MediaLink, index: int) -> object:
    if await _url_is_reachable(audio.url):
        return audio.url
    fallback_links = await _converted_links(data, "audio")
    return fallback_links[index].url if index < len(fallback_links) else audio.url


async def _send_audio(
    message: Message,
    url: object,
    caption: str | None = None,
    reply_markup=None,
) -> None:
    await message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    await message.reply_audio(
        url,
        title=AUDIO_TITLE,
        performer=AUDIO_PERFORMER,
        caption=caption,
        reply_markup=reply_markup,
    )


async def _send_audio_with_fallback(
    message: Message,
    data: ResponseUtility,
    audio: MediaLink,
    index: int = 0,
    caption: str | None = None,
    reply_markup=None,
) -> None:
    url = await _audio_url(data, audio, index)
    try:
        await _send_audio(message, url, caption=caption, reply_markup=reply_markup)
    except Exception:
        fallback_links = await _converted_links(data, "audio")
        if index < len(fallback_links):
            await _send_audio(
                message,
                fallback_links[index].url,
                caption=caption,
                reply_markup=reply_markup,
            )


async def reply_media_group(message: Message, data: ResponseUtility) -> None:
    visual_items, audio_items = _split_media(_links(data.result))
    if not visual_items and not audio_items:
        raise ValueError("Content API returned no supported media")

    # Send each visual item independently. Telegram albums require at least two
    # compatible items, while API responses may mix video, image, and document.
    for index, item in enumerate(visual_items):
        is_last_visual = index == len(visual_items) - 1
        has_audio = bool(audio_items)
        await _send_visual_with_fallback(
            message,
            item,
            data,
            caption=data.caption if is_last_visual and not has_audio else None,
            reply_markup=data.button if is_last_visual and not has_audio else None,
            fallback_index=_same_type_index(visual_items, index),
        )

    for index, audio in enumerate(audio_items):
        is_last_audio = index == len(audio_items) - 1
        await _send_audio_with_fallback(
            message,
            data,
            audio,
            index=index,
            caption=data.caption if is_last_audio else None,
            reply_markup=data.button if is_last_audio else None,
        )


async def reply_audio(message: Message, data: ResponseUtility) -> None:
    audio_links = [item for item in _links(data.result) if item.type.lower() == "audio"]
    if not audio_links:
        raise ValueError("Content API returned no audio media")
    await _send_audio_with_fallback(
        message,
        data,
        audio_links[0],
        caption=data.caption,
        reply_markup=data.button,
    )
