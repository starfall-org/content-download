from hydrogram.enums import ChatAction
from hydrogram.types import (
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from bot.schemas.api import ResponseGroup, ResponseItem
from bot.utils.convert_tools import item_to_io, list_to_io


def convert_input_media(
    media: list[ResponseItem],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return [
        InputMediaVideo(link.url)
        if link.mediatype == "video"
        else InputMediaPhoto(link.url)
        for link in media
    ]


async def reply_media_group(
    m: Message, media: ResponseGroup, button: InlineKeyboardMarkup, caption: str
) -> None:
    if not media.is_list:
        if media.content.mediatype == "video":
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(
                    media.content.url, reply_markup=button, caption=caption
                )
            except Exception:
                file = await item_to_io(media.content)
                await m.reply_video(file.url, reply_markup=button, caption=caption)
        elif media.content.mediatype == "photo":
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(
                    media.content.url, reply_markup=button, caption=caption
                )
            except Exception:
                file = await item_to_io(media.content)
                await m.reply_photo(file.url, reply_markup=button, caption=caption)
    else:
        items: list[ResponseItem] = media.content
        last_item = items[-1]
        for i in range(0, len(items) - 1, 10):
            part_items = items[i : min(i + 10, len(items) - 1)]
            if any(link.is_video for link in part_items):
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            else:
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                media_group = convert_input_media(part_items)
                await m.reply_media_group(media_group)
            except Exception:
                if any(link.is_video for link in part_items):
                    await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                else:
                    await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                part_files = await list_to_io(part_items)
                media_group = convert_input_media(part_files)
                await m.reply_media_group(media_group)

        if last_item.mediatype == "video":
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(last_item.url, caption=caption, reply_markup=button)
            except Exception:
                file = await item_to_io(last_item)
                await m.reply_video(file.url, caption=caption, reply_markup=button)

        elif last_item.mediatype == "photo":
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(last_item.url, caption=caption, reply_markup=button)
            except Exception:
                file = await item_to_io(last_item)
                await m.reply_photo(file.url, caption=caption, reply_markup=button)


async def reply_audio(
    m: Message, media: ResponseGroup, button: InlineKeyboardMarkup, caption: str
):
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    try:
        await m.reply_audio(media.content.url, caption=caption, reply_markup=button)
    except Exception:
        file = await item_to_io(media.content)
        await m.reply_audio(file.url, caption=caption, reply_markup=button)
