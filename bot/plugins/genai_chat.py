from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from hydrogram.types import Message

from bot.genai.core import GoogleGenAI

gg = GoogleGenAI()
OWNER_ID = 7642104102


@Client.on_message(filters.command("reset") & filters.user(OWNER_ID))
async def new_chat(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    gg.reset_chat()
    await m.reply("**New Chat Created**", quote=True)


@Client.on_message(filters.command("model"))
async def current_model(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    await m.reply(
        f"**Current Model:** `{gg.current_model()}`",
        quote=True,
    )


@Client.on_message(filters.command("models") & filters.user(7642104102))
async def list_models(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    models = gg.list_models()
    models = [f"`{model}`" for model in models]
    await m.reply("\n".join(models), quote=True)


@Client.on_message(filters.command("select") & filters.user(7642104102))
async def switch_model(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    if len(m.command) < 2:
        await m.reply("**Usage:** `/select model_name`", quote=True)
    model = m.command[1]
    models = gg.list_models()
    if model.startswith("gemini") and model in [md.split("/")[-1] for md in models]:
        gg.switch_model(model)
        await m.reply(f"**Model switched to:** `{model}`", quote=True)
    else:
        models = [f"`{model}`" for model in models]
        await m.reply(
            f"**Usage:** `/select model_name`\n**Available Models:**\n{', '.join(models)}",
            quote=True,
        )


@Client.on_message(filters.command("instruction") & filters.user(7642104102))
async def instruction_manage(c: Client, m: Message):
    await m.reply_chat_action(ChatAction.TYPING)
    current_instruction = gg.get_instruction()
    if len(m.command) < 2:
        await m.reply(
            f"**Usage:** `/instruction instruction`\n**Current Instruction:** ```\n{current_instruction}```",
            quote=True,
        )
        gg.set_instruction()
    else:
        instruction = m.command[1]
        gg.set_instruction(instruction)
    await m.reply(
        f"**Instruction was changed!**\n**From:** ```\n{current_instruction}```\n**To:** ```\n{instruction}```",
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
    aichat = gg.get_chat()
    try:
        text, media = await aichat.send(c, m)
    except Exception:
        aichat = gg.reset_chat()
        text, media = await aichat.send(c, m)
    if media:
        if media.mime_type.startswith("image/"):
            await m.reply_photo(photo=media.data, caption=text, quote=True)
        elif media.mime_type.startswith("video/"):
            await m.reply_video(video=media.data, caption=text, quote=True)
        elif media.mime_type.startswith("audio/"):
            await m.reply_audio(audio=media.data, caption=text, quote=True)
        else:
            await m.reply_document(document=media.data, caption=text, quote=True)
        text = ""
    else:
        await m.reply(text, quote=True)
