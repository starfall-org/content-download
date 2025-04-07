from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import Message

from bot.genai.core import GoogleGenAI

gg = GoogleGenAI()


@Client.on_message(filters.command("reset") & filters.private)
async def reset_chat(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    t = await m.reply_text("Resetting...")
    await gg.new_chat()
    await t.edit_text("Resetted!")


@Client.on_message(filters.command("model"))
async def current_model(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply(
        f"**Current Model:** `{gg.current_model()}`",
        quote=True,
    )


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
    text, medias = await gg.send_message(c, m)
    if medias:
        for media in medias:
            if media.mime_type.startswith("image/"):
                await m.reply_photo(photo=media.url, caption=text, quote=True)
            elif media.mime_type.startswith("video/"):
                await m.reply_video(video=media.url, caption=text, quote=True)
            elif media.mime_type.startswith("audio/"):
                await m.reply_audio(audio=media.url, caption=text, quote=True)
            else:
                await m.reply_document(document=media.url, caption=text, quote=True)
            text = ""
    else:
        await m.reply(text, quote=True)
