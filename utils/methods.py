from hydrogram.enums import ChatAction
from hydrogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    InlineKeyboardMarkup,
    Message,
)
from .models import Links, LinkInfo
from .tools import ionify


def __parse_media_group__(
    media: list[LinkInfo],
) -> list[InputMediaPhoto | InputMediaVideo]:
    return [
        InputMediaVideo(link.url) if link.is_video else InputMediaPhoto(link.url)
        for link in media
    ]


async def __parse_ionify__(media: list[LinkInfo]) -> list[LinkInfo]:
    return [LinkInfo(link.is_video, await ionify(link.url)) for link in media]


async def send_media(
    m: Message, media: Links, button: InlineKeyboardMarkup, caption: str
) -> None:
    if media.standalone:
        if media.content.is_video:
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(
                    media.content.url, reply_markup=button, caption=caption
                )
            except Exception:
                file = await ionify(media.content.url, ext="mp4")
                await m.reply_video(file, reply_markup=button, caption=caption)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(
                    media.content.url, reply_markup=button, caption=caption
                )
            except Exception:
                file = await ionify(media.content.url, ext="jpg")
                await m.reply_photo(file, reply_markup=button, caption=caption)
    else:
        links: list[LinkInfo] = media.content
        last_link = links[-1]
        for i in range(0, len(links) - 1, 10):
            part_links = links[i : min(i + 10, len(links) - 1)]
            if any(link.is_video for link in part_links):
                await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            else:
                await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                media_group = __parse_media_group__(part_links)
                await m.reply_media_group(media_group)
            except Exception:
                if any(link.is_video for link in part_links):
                    await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                else:
                    await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                part_files = await __parse_ionify__(part_links)
                media_group = __parse_media_group__(part_files)
                await m.reply_media_group(media_group)

        if last_link.is_video:
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(last_link.url, caption=caption, reply_markup=button)
            except Exception:
                file = await ionify(last_link.url, ext="mp4")
                await m.reply_video(file, caption=caption, reply_markup=button)

        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(last_link.url, caption=caption, reply_markup=button)
            except Exception:
                file = await ionify(last_link.url, ext="jpg")
                await m.reply_photo(file, caption=caption, reply_markup=button)


async def send_audio(
    m: Message, media: Links, button: InlineKeyboardMarkup, caption: str
):
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    try:
        await m.reply_audio(media.content.url, caption=caption, reply_markup=button)
    except Exception:
        file = await ionify(media.content.url, ext="mp3")
        await m.reply_audio(file, caption=caption, reply_markup=button)
