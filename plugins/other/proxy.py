from hydrogram import Client, filters
from ext import owner
import os

@Client.on_message(filters.command("proxy") & owner)
async def set_proxy(c, m):
    proxy = m.command[1]
    os.system("pkill -9 lite")
    os.system(f"./lite -p 8090 {proxy} &")
    await m.reply("Đã thiết lập proxy thành công")
    await m.delete()