from hydrogram import filters, Client, enums
from data import Get
from ext import owner

typing = enums.ChatAction.TYPING

@Client.on_message(filters.command("count") & owner)
def count_uses(c, m):
    m.reply_chat_action(typing)
    user, chat = Get.get_count()
    m.reply(f"Chats: {chat}\nUsers: {user}")


@Client.on_message(filters.command("users") & owner)
def users_list(c, m):
    m.reply_chat_action(typing)
    count, users = Get.users_list()
    m.reply(f"__--**{count}**--__")
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


@Client.on_message(filters.command("chats") & owner)
def chats_list(c, m):
    m.reply_chat_action(typing)
    count, chats = Get.chats_list()
    m.reply(f"__--**{count}**--__")
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
