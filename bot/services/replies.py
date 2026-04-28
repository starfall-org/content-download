from collections.abc import Iterable
from email.mime import audio

from aiohttp import ClientSession, ClientTimeout
from hydrogram.enums import ChatAction
from hydrogram.types import InputMediaPhoto, InputMediaVideo, Message

from bot.schemas.download import CommonLink, CommonLinks, YoutubeLink, YoutubeLinks
from bot.schemas.telegram import ResponseUtility
from bot.services.media_converter import convert_to_io

MediaLink = CommonLink | YoutubeLink

ALBUM_SIZE = 10
AUDIO_TITLE = "music"
AUDIO_PERFORMER = "music.mp3"


def _chunked(
    items: list[MediaLink],
    size: int = ALBUM_SIZE,
) -> Iterable[list[MediaLink]]:
    for index in range(0, len(items), size):
        yield items[index : index + size]


def _links(result: CommonLinks | YoutubeLinks) -> list[MediaLink]:
    if isinstance(result, CommonLinks):
        return result.links

    return [result.video, result.audio]


def _split_media(items: list[MediaLink]) -> tuple[list[MediaLink], list[MediaLink]]:
    audio = [item for item in items if item.type == "audio"]
    visual = [item for item in items if item.type != "audio"]
    return visual, audio


def _same_type_index(items: list[MediaLink], index: int) -> int:
    media_type = items[index].type
    return sum(item.type == media_type for item in items[: index + 1]) - 1


def _input_media(item: MediaLink) -> InputMediaPhoto | InputMediaVideo:
    if item.type == "video":
        return InputMediaVideo(item.url)

    return InputMediaPhoto(item.url)


def _input_media_group(
    items: list[MediaLink],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return [_input_media(item) for item in items]


def convert_input_media(
    media: list[MediaLink],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return _input_media_group(media)


def _chat_action(media_type: str) -> ChatAction:
    if media_type == "video":
        return ChatAction.UPLOAD_VIDEO
    if media_type == "audio":
        return ChatAction.UPLOAD_AUDIO
    return ChatAction.UPLOAD_PHOTO


def _album_action(items: list[MediaLink]) -> ChatAction:
    if any(item.type == "video" for item in items):
        return ChatAction.UPLOAD_VIDEO

    return ChatAction.UPLOAD_PHOTO


async def _converted_links(data: ResponseUtility, media_type: str) -> list[MediaLink]:
    converted = await convert_to_io(data.result)
    return [item for item in _links(converted) if item.type == media_type]


async def _send_visual(
    message: Message,
    item: MediaLink,
    caption: str | None = None,
    reply_markup=None,
) -> None:
    await message.reply_chat_action(_chat_action(item.type))

    reply_kwargs = {"reply_markup": reply_markup}
    if caption:
        reply_kwargs["caption"] = caption

    if item.type == "video":
        await message.reply_video(item.url, **reply_kwargs)
        return

    if item.type == "image":
        await message.reply_photo(item.url, **reply_kwargs)


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


async def _send_visual_album(
    message: Message,
    items: list[MediaLink],
    data: ResponseUtility,
) -> None:
    for chunk_index, chunk in enumerate(_chunked(items)):
        if not chunk:
            continue

        await message.reply_chat_action(_album_action(chunk))
        try:
            await message.reply_media_group(_input_media_group(chunk))
        except Exception:
            fallback = await convert_to_io(data.result)
            fallback_items = [
                item for item in _links(fallback) if item.type != "audio"
            ][chunk_index * ALBUM_SIZE : chunk_index * ALBUM_SIZE + len(chunk)]
            if fallback_items:
                await message.reply_media_group(_input_media_group(fallback_items))


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
    if index < len(fallback_links):
        return fallback_links[index].url

    return audio.url


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
        file_name="audio.mp3",
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

    if visual_items:
        has_audio = bool(audio_items)
        caption = None if has_audio else data.caption
        button = None if has_audio else data.button

        if len(visual_items) == 1:
            await _send_visual_with_fallback(
                message,
                visual_items[0],
                data,
                caption=caption,
                reply_markup=button,
            )
        else:
            album_items = visual_items[:-1]
            await _send_visual_album(message, album_items, data)
            await _send_visual_with_fallback(
                message,
                visual_items[-1],
                data,
                caption=caption,
                reply_markup=button,
                fallback_index=_same_type_index(visual_items, len(visual_items) - 1),
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
    audio_links = [item for item in _links(data.result) if item.type == "audio"]
    if not audio_links:
        return

    await _send_audio_with_fallback(
        message,
        data,
        audio_links[0],
        caption=data.caption,
        reply_markup=data.button,
    )
