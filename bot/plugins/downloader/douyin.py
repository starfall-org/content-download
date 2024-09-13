from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import save
from utils.tools import api_handler
from utils.methods import send_photos
from config import keys


@Client.on_message(filters.regex("http|https") & filters.regex("douyin."))
async def download_douyin(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    print(
        f"ACTION: douyin download\nCHAT: {m.chat.title} ({m.chat.id})\nUSER: {m.from_user.first_name} ({m.from_user.id})\nDATE: {m.date}",
        flush=True,
    )
    result = await api_handler(keys.douyin_api, m)
    if result.is_video:
        await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
        m.reply_video(result.result, caption=result.caption, reply_markup=result.button)
    else:
        await send_photos(m, result.result, result.button, result.caption)
    save(m)
    print("Douyin Done", flush=True)
    await m.delete()
