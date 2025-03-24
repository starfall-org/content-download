from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import Message

from bot.services.google_genai.core import GoogleGenAI

gg = GoogleGenAI()


@Client.on_message(
    (filters.private | filters.mentioned)
    & (
        ~filters.regex("http|https")
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
