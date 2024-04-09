from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from ext import owner
import subprocess
import sys
import os 

typing = ChatAction.TYPING

@Client.on_message(filters.command("update") & filters.private & owner)
async def system_update(c, m):
    await m.reply_chat_action(typing)
    result = subprocess.run(["./update.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    await m.reply(f"```bash\n{result.stdout}\n```")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@Client.on_message(filters.command("shell") & owner)
async def run_shell(c, m):
    await m.reply_chat_action(typing)
    command = m.text.replace("/shell ", "")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    await m.reply(f"```bash\n{result.stdout}\n```")