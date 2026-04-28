from collections.abc import Awaitable, Callable
from datetime import datetime

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.errors import Forbidden
from hydrogram.types import Message

from bot.config import logger
from bot.database import Database
from bot.schemas.telegram import ParsedChatArguments, ResponseUtility
from bot.services.content_api import get_api_result
from bot.services.replies import reply_audio, reply_media_group

DownloadReply = Callable[[Message, ResponseUtility], Awaitable[None]]

db = Database()

DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
MUSIC_COMMANDS = {"AUDIO", "MUSIC"}
URL_FILTER = filters.regex("http|https")


def _sender_name(message: Message) -> str:
    return (
        message.chat.full_name
        or getattr(message.from_user, "first_name", None)
        or getattr(message.sender_chat, "title", None)
        or "Unknown"
    )


def _chat_name(message: Message) -> str:
    return message.chat.title or message.chat.full_name or "Private"


def _log_download(message: Message, action: str) -> None:
    logger.info(
        (
            f"[{datetime.now().strftime(DATE_FORMAT)}]\n"
            f"SENDER: {_sender_name(message)}\n"
            f"CHAT: [{message.chat.id}] {_chat_name(message)}\n"
            f"ACTION: {action}"
        )
    )


def _is_music_request(message: Message) -> bool:
    return any(part.upper() in MUSIC_COMMANDS for part in (message.text or "").split())


async def _update_chat(message: Message, can_reply: bool) -> None:
    await db.update_chat(ParsedChatArguments(message=message, can_reply=can_reply))


async def _handle_download(
    message: Message,
    endpoint: str,
    action: str,
    reply: DownloadReply,
) -> None:
    await message.reply_chat_action(ChatAction.TYPING)

    try:
        result = await get_api_result(endpoint, message)
        await reply(message, result)
        await message.delete()
        _log_download(message, action)
        can_reply = True
    except Forbidden as error:
        logger.error(error)
        can_reply = False

    await _update_chat(message, can_reply)


@Client.on_message(URL_FILTER & filters.regex("youtube.|youtu.be"))
async def download_youtube(_: Client, message: Message) -> None:
    if _is_music_request(message):
        await _handle_download(message, "music", "music", reply_audio)
        return

    await _handle_download(message, "youtube", "youtube", reply_media_group)


@Client.on_message(URL_FILTER & filters.regex("facebook.|fb."))
async def download_facebook(_: Client, message: Message) -> None:
    await _handle_download(message, "facebook", "facebook", reply_media_group)


@Client.on_message(URL_FILTER & filters.regex("instagram."))
async def download_instagram(_: Client, message: Message) -> None:
    await _handle_download(message, "instagram", "instagram", reply_media_group)


@Client.on_message(URL_FILTER & filters.regex("douyin.|iesdouyin.|tiktok."))
async def download_douyin(_: Client, message: Message) -> None:
    await _handle_download(message, "douyin", "douyin", reply_media_group)
