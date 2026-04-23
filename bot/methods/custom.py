from hydrogram.enums import ChatAction
from hydrogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from bot.schemas.bot import ResponseUtility
from bot.schemas.common_link import CommonLink, CommonLinks
from bot.utils.convert_tools import convert_to_io


def convert_input_media(
    media: list[CommonLink],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return [
        InputMediaVideo(link.url) if link.type == "video" else InputMediaPhoto(link.url)
        for link in media
    ]


async def _ensure_common_links(data: ResponseUtility, use_fallback: bool) -> CommonLinks:
    result = data.result
    if use_fallback:
        result = await convert_to_io(result)
    return result


async def _reply_single_media(
    m: Message,
    media_index: int,
    data: ResponseUtility,
    *,
    use_fallback: bool = False,
) -> None:
    result = data.result
    if use_fallback:
        result = await _ensure_common_links(data, use_fallback)

    media = result.links[media_index]

    if media.type == "video":
        await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        await m.reply_video(media.url, reply_markup=data.button, caption=data.caption)
        return

    await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    await m.reply_photo(media.url, reply_markup=data.button, caption=data.caption)


async def reply_media_group(m: Message, data: ResponseUtility) -> None:
    if not isinstance(data.result, CommonLinks):
        raise TypeError("reply_media_group only supports CommonLinks responses")

    items = data.result.links
    if len(items) == 1:
        try:
            await _reply_single_media(m, 0, data)
        except Exception:
            await _reply_single_media(m, 0, data, use_fallback=True)
        return

    async def send_media_slice(part_items: list[CommonLink]) -> None:
        if any(link.type == "video" for link in part_items):
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        await m.reply_media_group(convert_input_media(part_items))

    for i in range(0, len(items) - 1, 10):
        part_items = items[i : min(i + 10, len(items) - 1)]
        try:
            await send_media_slice(part_items)
        except Exception:
            converted = await convert_to_io(data.result)
            await send_media_slice(converted.links[i : min(i + 10, len(items) - 1)])

    try:
        await _reply_single_media(m, len(items) - 1, data)
    except Exception:
        await _reply_single_media(m, len(items) - 1, data, use_fallback=True)


async def reply_audio(m: Message, data: ResponseUtility) -> None:
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    try:
        await m.reply_audio(
            data.audio.url, caption=data.caption, reply_markup=data.button
        )
    except Exception:
        result = await convert_to_io(data.result)
        await m.reply_audio(
            result.audio.url, caption=data.caption, reply_markup=data.button
        )
