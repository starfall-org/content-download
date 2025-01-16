from hydrogram import Client, filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from hydrogram.enums import ChatAction


@Client.on_message(filters.command(["start", "help"]) & filters.private)
async def reply_start(_: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply(
        "**Content Download Bot**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group", url="https://t.me/contentdownload_group"
                    ),
                    InlineKeyboardButton("Channel", url="https://t.me/contentdownload"),
                ],
            ]
        ),
    )
    print(
        f"ACTION: start bot\nUSER: {m.from_user.first_name} ({m.from_user.id})\nCHAT: {m.chat.title} ({m.chat.id})\nDATE: {m.date}",
        flush=True,
    )
