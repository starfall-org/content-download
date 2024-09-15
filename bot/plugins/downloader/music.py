from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import save
from utils.tools import api_handler, ionify
from config import keys


@Client.on_message(filters.command("music"))
async def download_music(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    print(
        f"ACTION: music download\n"
        f"CHAT: {m.chat.title} ({m.chat.id})\n"
        f"USER: {m.from_user.first_name if m.from_user else m.sender_chat.title} ({m.from_user.id if m.from_user else m.sender_chat.id})\n"
        f"DATE: {m.date}",
        flush=True,
    )
    result = await api_handler(keys.music_api, m)
    await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    try:
        await m.reply_audio(
            result.result, caption=result.caption, reply_markup=result.button
        )
    except Exception:
        iofile = await ionify(result.result)
        await m.reply_audio(iofile, caption=result.caption, reply_markup=result.button)
    save(m)
    print("Music Done", flush=True)
    await m.delete()
