from pyrogram import filters, Client
from api_callback.YTMusic import YTM
from utils.functions import save
from utils.variables import ra, sm, dl_ani, up_ani
import re, os, logging, time


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
  dw = m.reply_animation(dl_ani, quote=True)
  audio = YTM(url)
  c.delete_messages(m.chat.id, dw.id)
  uw = m.reply_animation(up_ani, quote=True)
  m.reply_audio(audio, caption=caption)
  c.delete_messages(m.chat.id, uw.id)
  try:
    m.delete()
  except Exception as e:
    delog = m.reply(e)
    time.sleep(5)
    c.delete_messages(m.chat.id, delog.id)
