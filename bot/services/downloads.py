from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Callable

from hydrogram.enums import ChatAction
from hydrogram.errors import Forbidden
from hydrogram.types import Message

from bot.config import logger
from bot.content_api import get_api_result
from bot.database.client import Database
from bot.methods.custom import reply_audio, reply_media_group
from bot.schemas.bot import ParsedChatArguments, ResponseUtility

ReplyHandler = Callable[[Message, ResponseUtility], Awaitable[None]]
YOUTUBE_AUDIO_COMMANDS = {"MUSIC", "AUDIO"}


@dataclass(frozen=True)
class DownloadTask:
    endpoint: str
    action_name: str
    reply_handler: ReplyHandler
    initial_chat_action: ChatAction = ChatAction.TYPING


def _get_sender_name(message: Message) -> str | None:
    return (
        message.chat.full_name
        or getattr(message.from_user, "first_name", None)
        or getattr(message.sender_chat, "title", None)
    )


def _get_chat_name(message: Message) -> str | None:
    return message.chat.title or message.chat.full_name


def _log_download(message: Message, action_name: str) -> None:
    logger.info(
        (
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]\n"
            f"SENDER: {_get_sender_name(message)}\n"
            f"CHAT: [{message.chat.id}] {_get_chat_name(message)}\n"
            f"ACTION: {action_name}"
        )
    )


async def _update_chat(message: Message, can_reply: bool) -> None:
    await Database.update_chat(
        ParsedChatArguments(
            message=message,
            can_reply=can_reply,
        )
    )


async def handle_download(message: Message, task: DownloadTask) -> None:
    await message.reply_chat_action(task.initial_chat_action)
    can_reply = False

    try:
        result = await get_api_result(task.endpoint, message)
        await task.reply_handler(message, result)
        await message.delete()
        _log_download(message, task.action_name)
        can_reply = True
    except Forbidden as exc:
        logger.error(exc)

    await _update_chat(message, can_reply)


def _is_audio_request(message: Message) -> bool:
    text = message.text or message.caption or ""
    return any(word.upper() in YOUTUBE_AUDIO_COMMANDS for word in text.split())


async def handle_youtube_download(message: Message) -> None:
    task = (
        DownloadTask(
            endpoint="music",
            action_name="music",
            reply_handler=reply_audio,
            initial_chat_action=ChatAction.UPLOAD_AUDIO,
        )
        if _is_audio_request(message)
        else DownloadTask(
            endpoint="youtube",
            action_name="youtube",
            reply_handler=reply_media_group,
        )
    )
    await handle_download(message, task)
