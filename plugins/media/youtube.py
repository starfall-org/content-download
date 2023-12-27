from api_callback.Youtube import YTDL,YTM, ODL
from etc.var import t, rv, ra, sv, sp, sm

def youtube(c, m, download, getattrs):
  url, original, button = getattrs(m=m)
  m.reply_chat_action(rv)
  file = YTDL(url)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(sv)
  sending = m.reply("**Sending**`...`", quote=True)
  s = m.reply_video(file, reply_markup=original, caption=caption)
  original = getattrs(s=s)
  c.edit_inline_reply_markup(s.id, original)
  c.delete_messages(m.chat.id, sending.id)
  try:
    m.delete()
  except:
    pass

def other(c, m, file, type, download, getattrs):
  _, original, button = getattrs(m=m)
  c.delete_messages(m.chat.id, download.id)
  m.reply_chat_action(t)
  sending = m.reply("**Sending**`...`", quote=True)
  s = None
  if type == "image":
    m.reply_chat_action(sp)
    s = m.reply_photo(file, reply_markup=original, caption=caption)
  elif type == "video":
    m.reply_chat_action(sv)
    s = m.reply_video(file, reply_markup=original, caption=caption)
  elif type == "audio":
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
  if s:
    original = getattrs(s=s)
    c.edit_inline_reply_markup(s.id, original)
  c.delete_messages(m.chat.id, sending.id)

def music(c, m, download, getattrs):
  url, _, caption = getattrs(m=m)
  m.reply_chat_action(ra)
  audio = YTM(url)
  c.delete_messages(m.chat.id, download.id)
  sending = m.reply("**Sending**`...`", quote=True)
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)
  c.delete_messages(m.chat.id, sending.id)