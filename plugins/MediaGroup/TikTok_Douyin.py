from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.TikTok_Douyin import TDDL
from utils.functions import save, send_photos, uploads
from utils.variables import sv, rv, dl_ani, up_ani
import re, os, logging, time


@Client.on_message(filters.regex(r"douyin.com|tiktok.com|iesdouyin.com"))
def handle_tiktokdouyin(c, m):
  save(m)
  text = m.text
  url = re.search(r"(?P<url>https?://[^\s]+)", text).group("url")
  original = InlineKeyboardMarkup([[InlineKeyboardButton("Original",
                                                         url=url)]])
  m.reply_chat_action(rv)
  try:
    user_name = m.sender_chat.title
    user_id = m.sender_chat.id
  except:
    user_name = m.from_user.first_name
    user_id = m.from_user.id
  caption = f'**[{user_name}](tg://user?id={user_id})**'
  dw = m.reply_animation(dl_ani, quote=True)
  file, is_video = TDDL(url)
  c.delete_messages(m.chat.id, dw.id)
  if is_video == False:
    send_photos(m, c, original, file, caption)
  elif is_video == True:
    uw = m.reply_animation(up_ani, quote=True)
    m.reply_chat_action(sv)
    m.reply_video(file, reply_markup=original, caption=caption)
    c.delete_messages(m.chat.id, uw.id)
    if m.chat.username == "contentdownload":
      uploads(file)
  try:
    m.delete()
  except Exception as e:
    delog = m.reply(e)
    time.sleep(5)
    c.delete_messages(m.chat.id, delog.id)
