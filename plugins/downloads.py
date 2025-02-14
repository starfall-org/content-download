from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import Message
from hydrogram.errors import Forbidden

from db.client import Database
from utils.methods import send_audio, send_media
from utils.tools import api_handler
from utils.models import LogMessage, ChatArgs

db = Database()


@Client.on_message(filters.regex("http|https") & filters.regex("youtube.|youtu.be"))
async def __youtube__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        if any(command.upper() in ["MUSIC", "AUDIO"] for command in m.text.split()):
            result = await api_handler("music", m)
            await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            await send_audio(m, result.result, result.button, result.caption)
            print(
                LogMessage(
                    action="music", user=m.from_user.id, message=m
                ).model_dump_json(),
                flush=True,
            )
        else:
            result = await api_handler("youtube", m)
            await send_media(m, result.result, result.button, result.caption)
            print(
                LogMessage(
                    action="youtube", user=m.from_user.id, message=m
                ).model_dump_json(),
                flush=True,
            )

        await m.delete()
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ChatArgs(
        message=m,
        can_reply=can_reply,
    )
    await db.save_chat(chat_args)


@Client.on_message(filters.regex("http|https") & filters.regex("facebook.|fb."))
async def __facebook__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        result = await api_handler("facebook", m)
        await send_media(m, result.result, result.button, result.caption)
        await m.delete()
        print(
            LogMessage(
                action="facebook", user=m.from_user.id, message=m
            ).model_dump_json(),
            flush=True,
        )
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ChatArgs(
        message=m,
        can_reply=can_reply,
    )
    await db.save_chat(chat_args)


@Client.on_message(filters.regex("http|https") & filters.regex("instagram."))
async def __instagram__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        result = await api_handler("instagram", m)
        await send_media(m, result.result, result.button, result.caption)
        await m.delete()
        print(
            LogMessage(
                action="instagram", user=m.from_user.id, message=m
            ).model_dump_json(),
            flush=True,
        )
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ChatArgs(
        message=m,
        can_reply=can_reply,
    )
    await db.save_chat(chat_args)


@Client.on_message(
    filters.regex("http|https") & filters.regex("douyin.|iesdouyin.|tiktok.")
)
async def __douyin__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        result = await api_handler("douyin", m)
        await send_media(m, result.result, result.button, result.caption)
        await m.delete()
        print(
            LogMessage(
                action="douyin", user=m.from_user.id, message=m
            ).model_dump_json(),
            flush=True,
        )
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ChatArgs(
        message=m,
        can_reply=can_reply,
    )
    await db.save_chat(chat_args)
