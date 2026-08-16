from aiohttp import ClientSession, ClientTimeout
from hydrogram.enums import ChatAction
from hydrogram.types import (
    InputMediaAudio,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from bot.schemas.download import CommonLink, CommonLinks
from bot.schemas.telegram import ResponseUtility
from bot.services.media_converter import convert_to_io

MediaLink = CommonLink
AUDIO_TITLE = "music"
AUDIO_PERFORMER = "music.mp3"
MEDIA_GROUP_LIMIT = 10


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


def _input_media(item: MediaLink):
    """Build an InputMedia object without putting captions on the album."""
    media_type = item.type.lower()
    if media_type == "image":
        return InputMediaPhoto(media=item.url)
    if media_type in {"video", "hls"}:
        return InputMediaVideo(media=item.url)
    if media_type == "document":
        return InputMediaDocument(media=item.url)
    raise ValueError(f"Unsupported media type: {item.type}")


def _media_group_kind(item: MediaLink) -> str:
    # Telegram permits photos and videos in one album, but documents must be
    # grouped only with documents. HLS is sent as a video after conversion.
    return "document" if item.type.lower() == "document" else "visual"


async def _send_visual_group(message: Message, items: list[MediaLink]) -> None:
    if len(items) == 1:
        await _send_visual(message, items[0])
        return
    await message.reply_chat_action(_chat_action(items[0].type))
    await message.reply_media_group(media=[_input_media(item) for item in items])


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


async def _send_visual_group_with_fallback(
    message: Message,
    items: list[MediaLink],
    data: ResponseUtility,
    all_items: list[MediaLink],
) -> None:
    try:
        await _send_visual_group(message, items)
        return
    except Exception:
        # A single bad URL must not prevent the rest of an album from being
        # delivered. Fall back per item, preserving the original order.
        for item in items:
            await _send_visual_with_fallback(
                message,
                item,
                data,
                fallback_index=_same_type_index(all_items, all_items.index(item)),
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


def _album_batches(items: list[MediaLink]) -> list[list[MediaLink]]:
    """Batch compatible items, leaving the response's final item alone."""
    if len(items) <= 1:
        return [items] if items else []

    batches: list[list[MediaLink]] = []
    pending: list[MediaLink] = []
    for item in items[:-1]:
        if pending and _media_group_kind(item) != _media_group_kind(pending[0]):
            batches.append(pending)
            pending = []
        pending.append(item)
        if len(pending) == MEDIA_GROUP_LIMIT:
            batches.append(pending)
            pending = []
    if pending:
        batches.append(pending)
    batches.append([items[-1]])
    return batches


async def reply_media_group(message: Message, data: ResponseUtility) -> None:
    visual_items, audio_items = _split_media(_links(data.result))
    if not visual_items and not audio_items:
        raise ValueError("Content API returned no supported media")

    # Albums are limited to ten items. Keep the final item separate so it can
    # carry the caption and button, while earlier items are sent in batches.
    for batch in _album_batches(visual_items):
        if len(batch) == 1 and batch[0] is visual_items[-1]:
            index = len(visual_items) - 1
            await _send_visual_with_fallback(
                message,
                batch[0],
                data,
                caption=data.caption if not audio_items else None,
                reply_markup=data.button if not audio_items else None,
                fallback_index=_same_type_index(visual_items, index),
            )
        else:
            await _send_visual_group_with_fallback(message, batch, data, visual_items)

    for batch in _audio_album_batches(audio_items):
        is_last_batch = batch[-1] is audio_items[-1]
        if is_last_batch and len(batch) == 1:
            index = len(audio_items) - 1
            await _send_audio_with_fallback(
                message,
                data,
                batch[0],
                index=index,
                caption=data.caption,
                reply_markup=data.button,
            )
            continue

        try:
            await _send_audio_group(message, batch)
        except Exception:
            for item in batch:
                index = audio_items.index(item)
                await _send_audio_with_fallback(message, data, item, index=index)


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


def _audio_media(item: MediaLink):
    return InputMediaAudio(media=item.url, title=AUDIO_TITLE, performer=AUDIO_PERFORMER)


async def _send_audio_group(message: Message, items: list[MediaLink]) -> None:
    if len(items) == 1:
        await _send_audio(message, items[0].url)
        return
    await message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    await message.reply_media_group(media=[_audio_media(item) for item in items])


def _audio_album_batches(items: list[MediaLink]) -> list[list[MediaLink]]:
    if len(items) <= 1:
        return [items] if items else []
    batches: list[list[MediaLink]] = []
    pending: list[MediaLink] = []
    for item in items[:-1]:
        pending.append(item)
        if len(pending) == MEDIA_GROUP_LIMIT:
            batches.append(pending)
            pending = []
    if pending:
        batches.append(pending)
    batches.append([items[-1]])
    return batches
