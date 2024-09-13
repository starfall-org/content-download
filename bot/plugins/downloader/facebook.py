from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import save
from utils.tools import api_handler
from utils.methods import send_photos, send_videos
from config import keys


@Client.on_message(filters.regex("http|https") & filters.regex("facebook.|fb."))
async def download_fb(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    print(
        f"ACTION: facebook download\nCHAT: {m.chat.title} ({m.chat.id})\nUSER: {m.from_user.first_name} ({m.from_user.id})\nDATE: {m.date}",
        flush=True,
    )
    result = await api_handler(keys.facebook_api, m)
    if result.is_video:
        if isinstance(result.result, list):
            await send_videos(m, result.result, result.button, result.caption)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            await m.reply_video(
                result.result, caption=result.caption, reply_markup=result.button
            )

    else:
        if isinstance(result.result, list):
            await send_photos(m, result.result, result.button, result.caption)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await m.reply_photo(
                result.result, caption=result.caption, reply_markup=result.button
            )
    save(m)
    print("Facebook Done", flush=True)
    await m.delete()
