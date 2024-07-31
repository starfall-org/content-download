from pyrogram import filters, Client, enums
from database import Get

typing = enums.ChatAction.TYPING


def _owner(_, __, m):
    return (
        m.from_user.id == 5665225938
        if m.from_user
        else m.sender_chat.username == "contentdownload"
    )


@Client.on_message(filters.command("count") & filters.create(_owner))
def count_uses(c, m):
    m.reply_chat_action(typing)
    user, chat = Get.get_count()
    m.reply(f"Chats: {chat}\nUsers: {user}")


@Client.on_message(filters.command("users") & filters.create(_owner))
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


@Client.on_message(filters.command("chats") & filters.create(_owner))
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


@Client.on_message(filters.command("myactivity"))
def get_start_time(c, m):
    if m.from_user:
        first_time, on_chat, on_with, msg_count = Get.user_history(m.from_user.id)
        if m.from_user.language_code == "vi":
            m.reply(
                f"Bạn bắt đầu sử dụng bot **{on_with}** từ ngày --**{first_time}**-- tại cuộc trò chuyện __--**{on_chat}**--__.\nBạn đã nhắn tổng cộng __--{msg_count}--__ tin nhắn",
                quote=True,
            )
