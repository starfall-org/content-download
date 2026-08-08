from collections.abc import Awaitable, Callable
from datetime import datetime
from urllib.parse import urlsplit

from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.errors import Forbidden
from hydrogram.types import Message

from bot.config import logger
from bot.database import Database
from bot.schemas.telegram import ParsedChatArguments, ResponseUtility
from bot.services.content_api import get_api_result
from bot.services.replies import reply_audio, reply_media_group
from bot.telegram.parsing import parse_attributes

DownloadReply = Callable[[Message, ResponseUtility], Awaitable[None]]

DB = Database()
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
MUSIC_COMMANDS = {"AUDIO", "MUSIC"}
URL_FILTER = filters.regex(r"https?://")
PLATFORMS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("youtube.com", "youtu.be"), "youtube"),
    (("facebook.com", "fb.watch"), "facebook"),
    (("instagram.com",), "instagram"),
    (("douyin.com", "iesdouyin.com", "tiktok.com"), "douyin"),
    (("bilibili.com", "b23.tv"), "bilibili"),
    (("xiaohongshu.com", "xhslink.com", "xhslink.cn"), "xhs"),
    (("hoyolab.com",), "hoyolab"),
    (("x.com", "twitter.com", "t.co"), "x"),
)


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
        f"[{datetime.now().strftime(DATE_FORMAT)}]\n"
        f"SENDER: {_sender_name(message)}\n"
        f"CHAT: [{message.chat.id}] {_chat_name(message)}\n"
        f"ACTION: {action}"
    )


def _is_music_request(message: Message) -> bool:
    return any(part.upper() in MUSIC_COMMANDS for part in (message.text or "").split())


def _platform_for_url(url: str) -> str | None:
    hostname = (urlsplit(url).hostname or "").lower()
    for domains, endpoint in PLATFORMS:
        if any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains):
            return endpoint
    return None


async def _update_chat(message: Message, can_reply: bool) -> None:
    await DB.update_chat(ParsedChatArguments(message=message, can_reply=can_reply))


async def _handle_download(
    message: Message,
    endpoint: str,
    reply: DownloadReply,
) -> None:
    await message.reply_chat_action(ChatAction.TYPING)
    can_reply = True
    try:
        result = await get_api_result(endpoint, message)
        await reply(message, result)
        await message.delete()
        _log_download(message, endpoint)
    except Forbidden as error:
        logger.error(error)
        can_reply = False
    except Exception as error:
        logger.exception("%s download failed: %s", endpoint, error)
        try:
            await message.reply(f"Unable to download this content: {error}")
        except Forbidden:
            can_reply = False

    await _update_chat(message, can_reply)


@Client.on_message(URL_FILTER)
async def download_content(_: Client, message: Message) -> None:
    try:
        attrs = parse_attributes(message)
    except ValueError:
        return

    endpoint = _platform_for_url(attrs.url)
    if not endpoint:
        return

    if endpoint == "youtube" and _is_music_request(message):
        await _handle_download(message, "youtube", reply_audio)
    else:
        await _handle_download(message, endpoint, reply_media_group)
