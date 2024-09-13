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
        f"ACTION: music download\nCHAT: {m.chat.title} ({m.chat.id})\nUSER: {m.from_user.first_name} ({m.from_user.id})\nDATE: {m.date}",
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
