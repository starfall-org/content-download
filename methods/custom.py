from hydrogram.enums import ChatAction
from hydrogram.types import (
    InlineKeyboardMarkup,
    Message,
)

from models.api_models import APIResultGroup, APIResult

from .util import list_to_io, parse_media_group, url_to_io


async def reply_media_group(
    m: Message, media: APIResultGroup, button: InlineKeyboardMarkup, caption: str
) -> None:
    if media.standalone:
        if media.content.is_video:
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(
                    media.content.url, reply_markup=button, caption=caption
                )
            except Exception:
                file = await url_to_io(
                    media.content.url, title=media.content.title, ext="mp4"
                )
                await m.reply_video(file, reply_markup=button, caption=caption)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(
                    media.content.url, reply_markup=button, caption=caption
                )
            except Exception:
                file = await url_to_io(
                    media.content.url, title=media.content.title, ext="jpg"
                )
                await m.reply_photo(file, reply_markup=button, caption=caption)
    else:
        links: list[APIResult] = media.content
        last_link = links[-1]
        for i in range(0, len(links) - 1, 10):
            part_links = links[i : min(i + 10, len(links) - 1)]
            if any(link.is_video for link in part_links):
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            else:
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                media_group = parse_media_group(part_links)
                await m.reply_media_group(media_group)
            except Exception:
                if any(link.is_video for link in part_links):
                    await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                else:
                    await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                part_files = await list_to_io(part_links)
                media_group = parse_media_group(part_files)
                await m.reply_media_group(media_group)

        if last_link.is_video:
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(last_link.url, caption=caption, reply_markup=button)
            except Exception:
                file = await url_to_io(last_link.url, title=last_link.title, ext="mp4")
                await m.reply_video(file, caption=caption, reply_markup=button)

        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(last_link.url, caption=caption, reply_markup=button)
            except Exception:
                file = await url_to_io(last_link.url, title=last_link.title, ext="jpg")
                await m.reply_photo(file, caption=caption, reply_markup=button)


async def reply_audio(
    m: Message, media: APIResultGroup, button: InlineKeyboardMarkup, caption: str
):
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    try:
        await m.reply_audio(media.content.url, caption=caption, reply_markup=button)
    except Exception:
        file = await url_to_io(media.content.url, ext="mp3", title=media.content.title)
        await m.reply_audio(file, caption=caption, reply_markup=button)
