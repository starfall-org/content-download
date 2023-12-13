from pyrogram import filters, Client
from api_callback.YTMusic import YTM
from utils.etc import save
from utils.var import ra, sm
import re


@Client.on_message(filters.command("music"))
def handle_music(c, m):
  save(m)
  m.reply_chat_action(ra)
  text = m.text
  url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  download = m.reply("**Downloading**`...`", quote=True)
  audio = YTM(url)
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)
  c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except:
    pass