from datetime import datetime

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.errors import Forbidden
from hydrogram.types import Message

from database.client import Database
from methods.custom import reply_media_group, reply_audio
from models.bot_models import ParsedChatArguments
from services.api.core import get_api_result

db = Database()


@Client.on_message(filters.regex("http|https") & filters.regex("youtube.|youtu.be"))
async def __youtube__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        if any(command.upper() in ["MUSIC", "AUDIO"] for command in m.text.split()):
            result = await get_api_result("music", m)
            await m.reply_chat_action(ChatAction.UPLOAD_AUDIO)
            await reply_audio(m, result.result, result.button, result.caption)
            print(
                (
                    f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
                    f"SENDER: {m.chat.full_name or getattr(m.from_user, 'first_name') or getattr(m.sender_chat, 'title')}\n"
                    f"CHAT: [{m.chat.id}] {m.chat.title or m.chat.full_name}\n"
                    "ACTION: music"
                ),
                flush=True,
            )
        else:
            result = await get_api_result("youtube", m)
            await reply_media_group(m, result.result, result.button, result.caption)
            print(
                (
                    f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
                    f"SENDER: {m.chat.full_name or getattr(m.from_user, 'first_name') or getattr(m.sender_chat, 'title')}\n"
                    f"CHAT: [{m.chat.id}] {m.chat.title or m.chat.full_name}\n"
                    "ACTION: youtube"
                ),
                flush=True,
            )

        await m.delete()
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ParsedChatArguments(
        message=m,
        can_reply=can_reply,
    )
    await db.update_chat(chat_args)


@Client.on_message(filters.regex("http|https") & filters.regex("facebook.|fb."))
async def __facebook__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        result = await get_api_result("facebook", m)
        await reply_media_group(m, result.result, result.button, result.caption)
        await m.delete()
        print(
            (
                f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
                f"SENDER: {m.chat.full_name or getattr(m.from_user, 'first_name') or getattr(m.sender_chat, 'title')}\n"
                f"CHAT: [{m.chat.id}] {m.chat.title or m.chat.full_name}\n"
                "ACTION: facebook"
            ),
            flush=True,
        )
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ParsedChatArguments(
        message=m,
        can_reply=can_reply,
    )
    await db.update_chat(chat_args)


@Client.on_message(filters.regex("http|https") & filters.regex("instagram."))
async def __instagram__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        result = await get_api_result("instagram", m)
        await reply_media_group(m, result.result, result.button, result.caption)
        await m.delete()

        print(
            (
                f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
                f"SENDER: {m.chat.full_name or getattr(m.from_user, 'first_name') or getattr(m.sender_chat, 'title')}\n"
                f"CHAT: [{m.chat.id}] {m.chat.title or m.chat.full_name}\n"
                "ACTION: instagram"
            ),
            flush=True,
        )
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ParsedChatArguments(
        message=m,
        can_reply=can_reply,
    )
    await db.update_chat(chat_args)


@Client.on_message(
    filters.regex("http|https") & filters.regex("douyin.|iesdouyin.|tiktok.")
)
async def __douyin__(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    try:
        result = await get_api_result("douyin", m)
        await reply_media_group(m, result.result, result.button, result.caption)
        await m.delete()
        print(
            (
                f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
                f"SENDER: {m.chat.full_name or getattr(m.from_user, 'first_name') or getattr(m.sender_chat, 'title')}\n"
                f"CHAT: [{m.chat.id}] {m.chat.title or m.chat.full_name}\n"
                "ACTION: douyin"
            ),
            flush=True,
        )
        can_reply = True
    except Forbidden:
        can_reply = False

    chat_args = ParsedChatArguments(
        message=m,
        can_reply=can_reply,
    )
    await db.update_chat(chat_args)
