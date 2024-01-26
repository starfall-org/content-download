from hydrogram import Client, filters
from ext import owner
import subprocess

@Client.on_message(filters.command("proxy") & owner)
def set_proxy(c, m):
    proxy = m.command[1]
    subprocess.run(["./lite", proxy], shell=True)
    m.reply("Đã thiết lập proxy thành công")
    m.delete()