from pyrogram import filters, Client, enums
from data import get_chats, get_users

typing = enums.ChatAction.TYPING

@Client.on_message(filters.command("count"))
def uses_count(c, m):
    m.reply_chat_action(t)
    user, _ = get_users()
    chat, __ = get_chats()
    m.reply(f"Chats: {chat}\nUsers: {user}")


@Client.on_message(filters.command("users") & filters.private)
def users_list(c, m):
    m.reply_chat_action(typing)
    count, users = get_users()
    m.reply(count)
    message = ""
    for i, user in enumerate(users):
        message += f"{i+1}) {user}\n"
        if len(message) >= 4090:
            m.reply_chat_action(typing)
            m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
            message = ""
    if message:
        m.reply_chat_action(typing)
        m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command("chats") & filters.private)
def chats_list(c, m):
    m.reply_chat_action(typing)
    count, chats = get_chats()
    m.reply(count)
    message = ""
    for i, chat in enumerate(chats):
        message += f"{i+1}) {chat}\n"
        if len(message) >= 4090:
            m.reply_chat_action(typing)
            m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
            message = ""
    if message:
        m.reply_chat_action(typing)
        m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
