from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from utils.db import save
from utils.tools import api_handler, ionify
from utils.methods import send_photos
from config import keys


@Client.on_message(
    filters.regex("http|https") & filters.regex("douyin.|iesdouyin.|tiktok.")
)
async def download_douyin(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    print(
        f"ACTION: douyin download\nCHAT: {m.chat.title} ({m.chat.id})\nUSER: {m.from_user.first_name} ({m.from_user.id})\nDATE: {m.date}",
        flush=True,
    )
    result = await api_handler(keys.douyin_api, m)
    if result.is_video:
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
        try:
            await send_photos(m, result.result, result.button, result.caption)
        except Exception:
            iofile = [await ionify(i) for i in result.result]
            await send_photos(m, iofile, result.button, result.caption)
    save(m)
    print("Douyin Done", flush=True)
    await m.delete()
