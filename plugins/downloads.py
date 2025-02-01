from hydrogram import Client, filters, API
from hydrogram.types import Message
from hydrogram.enums import ChatAction
from utils.tools import api_handler
from utils.methods import send_media, send_audio
from db import save


def __print__(m: Message, platform: str):
    print(
        f"ACTION: {platform} download\n"
        f"CHAT: {m.chat.title} ({m.chat.id})\n"
        f"USER: {m.from_user.first_name if m.from_user else m.sender_chat.title} ({m.from_user.id if m.from_user else m.sender_chat.id})\n"
        f"DATE: {m.date}"
        f"STATUS: success",
        flush=True,
    )


@Client.on_message(filters.regex("http|https") & filters.regex("youtube.|youtu.be"))
async def __youtube__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    if any(command.upper() in ["MUSIC", "AUDIO"] for command in m.text.split()):
        result = await api_handler("music", m)
        await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
        await send_audio(m, result.result, result.button, result.caption)
        __print__(m, "music")
    else:
        result = await api_handler("youtube", m)
        await send_media(m, result.result, result.button, result.caption)
        __print__(m, "youtube")
    await save(m)
    await m.delete()


@Client.on_message(filters.regex("http|https") & filters.regex("facebook.|fb."))
async def __facebook__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    result = await api_handler("facebook", m)
    await send_media(m, result.result, result.button, result.caption)
    await save(m)
    await m.delete()
    __print__(m, "facebook")


@Client.on_message(filters.regex("http|https") & filters.regex("instagram."))
async def __instagram__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    retry_count = 0
    while True:
        if retry_count > 5:
            print("RETRYING: TIMEOUT! ---> EXIT", flush=True)
            return

        try:
            result = await api_handler("instagram", m)
            break
        except Exception:
            retry_count += 1
            print(f"RETRYING: {retry_count} ---> CONTINUE", flush=True)

    await send_media(m, result.result, result.button, result.caption)
    await save(m)
    await m.delete()
    __print__(m, "instagram")


@Client.on_message(
    filters.regex("http|https") & filters.regex("douyin.|iesdouyin.|tiktok.")
)
async def __douyin__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    result = await api_handler("douyin", m)
    await send_media(m, result.result, result.button, result.caption)
    await save(m)
    await m.delete()
    __print__(m, "douyin")
