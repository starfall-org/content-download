from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import save
from utils.tools import api_handler, ionify
from utils.methods import send_photos, send_videos
from config import keys


@Client.on_message(filters.regex("http|https") & filters.regex("instagram."))
async def download_ig(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    print(
        f"ACTION: instagram download\n"
        f"CHAT: {m.chat.title} ({m.chat.id})\n"
        f"USER: {m.from_user.first_name if m.from_user else m.sender_chat.title} ({m.from_user.id if m.from_user else m.sender_chat.id})\n"
        f"DATE: {m.date}",
        flush=True,
    )
    result = await api_handler(keys.instagram_api, m)
    if result.is_video:
        if isinstance(result.result, list):
            try:
                await send_videos(m, result.result, result.button, result.caption)
            except Exception:
                iofile = [await ionify(i) for i in result.result]
                await send_videos(m, iofile, result.button, result.caption)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
            try:
                await m.reply_video(
                    result.result, caption=result.caption, reply_markup=result.button
                )
            except Exception:
                iofile = await ionify(result.result)
                await m.reply_video(
                    iofile, caption=result.caption, reply_markup=result.button
                )
    else:
        if isinstance(result.result, list):
            try:
                await send_photos(m, result.result, result.button, result.caption)
            except Exception:
                iofile = [await ionify(i) for i in result.result]
                await send_photos(m, iofile, result.button, result.caption)
        else:
            await m.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            try:
                await m.reply_photo(
                    result.result, caption=result.caption, reply_markup=result.button
                )
            except Exception:
                iofile = await ionify(result.result)
                await m.reply_photo(
                    iofile, caption=result.caption, reply_markup=result.button
                )
    save(m)
    print("Instagram Done", flush=True)
    await m.delete()
