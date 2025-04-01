from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import Message

from bot.services.google_genai.core import GoogleGenAI

gg = GoogleGenAI()


@Client.on_message(filters.command("reset") & filters.private)
async def reset_chat(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    t = await m.reply_text("Resetting...")
    await gg.new_chat()
    await t.edit_text("Resetted!")


@Client.on_message(
    (filters.private | filters.mentioned)
    & (
        ~filters.create(lambda _, __, m: m.text.startswith("/"))
        & ~filters.regex("http|https")
        & (
            ~filters.regex("youtube.|youtu.be")
            & ~filters.regex("facebook.|fb.")
            & ~filters.regex("instagram.")
            & ~filters.regex("douyin.|iesdouyin.|tiktok.")
        )
    )
)
async def genai_chat(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    response = await gg.send_message(c, m)
    await m.reply_text(response.text, quote=True)
