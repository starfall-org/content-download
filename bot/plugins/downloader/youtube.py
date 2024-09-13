from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import save
from utils.tools import api_handler
from config import keys


@Client.on_message(filters.regex("http|https") & filters.regex("youtube.|youtu.be"))
async def download_youtube(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    print(
        f"ACTION: youtube download\nCHAT: {m.chat.title} ({m.chat.id})\nUSER: {m.from_user.first_name} ({m.from_user.id})\nDATE: {m.date}",
        flush=True,
    )
    result = await api_handler(keys.yapi, m)
    await m.reply_chat_action(ChatAction.UPLOAD_VIDEO)
    await m.reply_video(
        result.result, caption=result.caption, reply_markup=result.button
    )
    save(m)
    print("Youtube Done", flush=True)
    await m.delete()
