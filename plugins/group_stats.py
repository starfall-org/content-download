from hydrogram import Client, filters
from hydrogram.types import ChatMemberUpdated
from db.client import Database

db = Database()


@Client.on_chat_member_updated
async def group_stats(c: Client, cmu: ChatMemberUpdated):
    member_count = await c.get_chat_members_count(cmu.chat.id)
    db.update_group_stats(cmu.chat, member_count)
