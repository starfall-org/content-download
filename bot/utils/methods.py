from typing import List

from pyrogram.enums import ChatAction
from pyrogram.types import (
    InputMediaPhoto,
    InputMediaVideo,
    InlineKeyboardMarkup,
    Message,
)


async def send_photos(
    m: Message, photo_links: List[str], button: InlineKeyboardMarkup, caption: str
) -> None:
    await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    if len(photo_links) == 1:
        await m.reply_photo(photo_links[0], reply_markup=button, caption=caption)
    else:
        for i in range(0, len(photo_links) - 1, 10):
            media_group = [
                InputMediaPhoto(link)
                for link in photo_links[i : min(i + 10, len(photo_links) - 1)]
            ]
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await m.reply_media_group(media_group)
        await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
        await m.reply_photo(photo_links[-1], caption=caption, reply_markup=button)


async def send_videos(
    m: Message, video_links: List[str], button: InlineKeyboardMarkup, caption: str
) -> None:
    await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
    if len(video_links) == 1:
        await m.reply_video(video_links[0], reply_markup=button, caption=caption)
    else:
        for i in range(0, len(video_links) - 1, 10):
            media_group = [
                InputMediaVideo(link)
                for link in video_links[i : min(i + 10, len(video_links) - 1)]
            ]
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            await m.reply_media_group(media_group)
        await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        await m.reply_video(video_links[-1], caption=caption, reply_markup=button)
