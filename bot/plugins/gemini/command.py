from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .gemini import Gemini
from utils.db.gemini.db import Database

ai = Gemini()


def _allowed(_, __, m):
    db = Database()
    return db.get(m.chat.id)


@Client.on_message(filters.command("reset") & filters.create(_allowed))
def refresh_chat(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    ai.reset()
    model_name = ai.info()
    m.reply(f"**{model_name}**")
    m.delete()


def _file_message(_, __, m):
    return m.reply_to_message and (
        m.reply_to_message.photo or m.reply_to_message.video or m.reply_to_message.audio
    )


@Client.on_message(filters.command("model") & filters.create(_allowed))
def get_models(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    buttons = [
        [InlineKeyboardButton(text=model.display_name, callback_data=model.name)]
        for model in ai.models()
    ]
    m.reply(
        "**AI Models**",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.MARKDOWN,
    )
    m.delete()


@Client.on_callback_query()
def handle_model(c, m):
    global ai
    model_name = m.data.split("/")[1]
    ai = Gemini(model_name)
    m.message.delete()
    m.answer("Model changed")


@Client.on_message(
    (filters.mentioned | filters.private)
    & ((filters.photo | filters.video | filters.audio) | filters.create(_file_message))
    & filters.create(_allowed)
    & filters.incoming
)
def handle_file(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    try:
        if m.reply_to_message:
            text = m.text
            file = c.download_media(m.reply_to_message, in_memory=True)
            if m.reply_to_message.photo:
                file_obj = {"mime_type": "image/png", "data": file.getvalue()}
            elif m.reply_to_message.audio:
                file_obj = {"mime_type": "audio/mpeg", "data": file.getvalue()}
            else:
                file_obj = {"mime_type": "video/mp4", "data": file.getvalue()}
        else:
            raise
    except Exception as e:
        print(e)
        text = m.caption
        file = c.download_media(m, in_memory=True)
        if m.photo:
            file_obj = {"mime_type": "image/png", "data": file.getvalue()}
        elif m.audio:
            file_obj = {"mime_type": "audio/mpeg", "data": file.getvalue()}
        else:
            file_obj = {"mime_type": "video/mp4", "data": file.getvalue()}
    if not text:
        text = "Nói về bức hình này đi"
    if text.startswith("@"):
        text = text.split(" ", 1)[1]
    try:
        if m.from_user:
            user = m.from_user
        else:
            user = m.sender_chat
        res = ai.send(m, text, user, file_obj)
        m.reply_chat_action(ChatAction.TYPING)
        m.reply(res, quote=True, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        m.reply(str(e), quote=True)


def _not_command(_, __, m):
    return not m.text.startswith("/")


@Client.on_message(
    (filters.mentioned | filters.private)
    & filters.text
    & filters.incoming
    & filters.create(_not_command)
    & filters.create(_allowed)
)
def handle_text(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    if m.text.startswith("@"):
        text = m.text.split(" ", 1)[1]
    else:
        text = m.text
    if m.from_user:
        user = m.from_user
    else:
        user = m.sender_chat
    try:
        res = ai.send(m, text, user)
        m.reply_chat_action(ChatAction.TYPING)
        m.reply(res, quote=True, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        m.reply(str(e), quote=True)
