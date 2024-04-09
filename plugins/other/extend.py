from hydrogram import filters, Client, enums
from data import Get
from ext import owner

typing = enums.ChatAction.TYPING

@Client.on_message(filters.command("count") & owner)
async def count_uses(c, m):
    await m.reply_chat_action(typing)
    user, chat = Get.get_count()
    await m.reply(f"Chats: {chat}\nUsers: {user}")


@Client.on_message(filters.command("users") & owner)
async def users_list(c, m):
    await m.reply_chat_action(typing)
    count, users = Get.users_list()
    await m.reply(f"__--**{count}**--__")
    message = ""
    for i, user in enumerate(users):
        message += f"{i+1}) {user}\n"
        if len(message) >= 4090:
            await m.reply_chat_action(typing)
            await m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
            message = ""
    if message:
        await m.reply_chat_action(typing)
        await m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.command("chats") & owner)
async def chats_list(c, m):
    await m.reply_chat_action(typing)
    count, chats = Get.chats_list()
    await m.reply(f"__--**{count}**--__")
    message = ""
    for i, chat in enumerate(chats):
        message += f"{i+1}) {chat}\n"
        if len(message) >= 4090:
            await m.reply_chat_action(typing)
            await m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)
            message = ""
    if message:
        await m.reply_chat_action(typing)
        await m.reply(message, quote=True, parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.command("when"))
async def get_start_time(c, m):
    if m.from_user:
        first_time, on_chat, on_with, msg_count = Get.user_history(m.from_user.id)
        if m.from_user.language_code == "vi":
            await m.reply(f"Bạn bắt đầu sử dụng bot **{on_with}** từ ngày --**{first_time}**-- tại cuộc trò chuyện __--**{on_chat}**--__.\nBạn đã nhắn tổng cộng __--{msg_count}--__ tin nhắn", quote=True)