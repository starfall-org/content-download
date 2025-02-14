from hydrogram import Client, filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram.enums import ChatAction
from db.client import Database
from utils.models import LogMessage

db = Database()


@Client.on_message(filters.command(["start", "help"]) & filters.private)
async def reply_start(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    text = (
        await db.get_preset("start_message")
        or "Welcome! Send a link and I'll send you the content."
    )
    panel_link = await db.get_preset("panel_link")
    await m.reply(
        f"**Content Downloa**\n\n{text}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group", url="https://t.me/contentdownload_group"
                    ),
                    InlineKeyboardButton("Channel", url="https://t.me/contentdownload"),
                    InlineKeyboardButton("Panel", url=panel_link),
                ],
            ]
        ),
    )
    print(
        LogMessage(
            action="start", user=m.from_user.first_name, message=m
        ).model_dump_json(),
        flush=True,
    )
