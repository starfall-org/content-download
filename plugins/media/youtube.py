from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api_callback.Youtube import YTDL,YTM, ODL
from etc.var import t, rv, ra, sv, sp, sm

def youtube(c, m):
  m.reply_chat_action(rv)
  file = YTDL(url)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(sv)
  sending = m.reply("**Sending**`...`", quote=True)
  m.reply_video(file, reply_markup=original, caption=caption)
  c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except:
    pass

def other(c, m):
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(t)
  sending = m.reply("**Sending**`...`", quote=True)
  if type == "image":
    m.reply_chat_action(sp)
    m.reply_photo(file, reply_markup=original, caption=caption)
  elif type == "video":
    m.reply_chat_action(sv)
    m.reply_video(file, reply_markup=original, caption=caption)
  elif type == "audio":
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
  c.delete_messages(m.chat.id, sending.id)

def music(c, m):
  m.reply_chat_action(ra)
  audio = YTM(url)
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)
  c.delete_messages(m.chat.id, sending.id)