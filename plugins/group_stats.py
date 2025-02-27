from hydrogram import Client, filters
from hydrogram.types import ChatMemberUpdated, Message
from hydrogram.enums import ChatAction
from db.client import Database
from utils.tools import plot_time_series

db = Database()


@Client.on_chat_member_updated
async def group_stats(c: Client, cmu: ChatMemberUpdated):
    member_count = await c.get_chat_members_count(cmu.chat.id)
    db.update_group_stats(cmu.chat, member_count)


@Client.on_message(filters.command("graph"))
async def graph(c: Client, m: Message):
    await c.send_chat_action(m.chat.id, ChatAction.TYPING)
    group_stats = db.get_current_group_stats(m.chat.id)
    if not group_stats:
        await m.reply("No data found.", quote=True)
        return
    path = plot_time_series(group_stats.member_count, group_stats)
    await m.reply_photo(path, quote=True)
