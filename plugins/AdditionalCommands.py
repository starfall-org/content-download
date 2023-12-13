from pyrogram import filters, Client, enums
from utils.db import get_chats, get_users
from utils.var import t


@Client.on_message(filters.command("count"))
def count(c, m):
  m.reply_chat_action(t)
  user, _ = get_users()
  chat, __ = get_chats()
  m.reply(f"Chats: {chat}\nUsers: {user}")


@Client.on_message(filters.command("users") & filters.private)
def users_list(c, m):
  m.reply_chat_action(t)
  _, users = get_users()
  m.reply(_)
  message = ""
  for i, user in enumerate(users):
    message += f"{i+1}) {user}\n"
    if len(message) >= 4090:
      m.reply_chat_action(t)
      m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
      message = ""
  if message:
    m.reply_chat_action(t)
    m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command("chats") & filters.private)
def chats_list(c, m):
  m.reply_chat_action(t)
  _, chats = get_chats()
  m.reply(_)
  message = ""
  for i, chat in enumerate(chats):
    message += f"{i+1}) {chat}\n"
    if len(message) >= 4090:
      m.reply_chat_action(t)
      m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
      message = ""
  if message:
    m.reply_chat_action(t)
    m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
