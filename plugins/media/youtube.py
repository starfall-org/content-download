from api_callback.Youtube import YTDL,YTM, ODL
from etc.var import t, rv, ra, sv, sp, sm

def youtube(c, m, status, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  file = YTDL(url)
  m.reply_chat_action(sv)
  status.edit("**Sending**`...`")
  s = m.reply_video(file, reply_markup=original, caption=caption)
  original = getattrs(m, s)
  s.edit_reply_markup(original)
  status.delete()
  try:
    m.delete()
  except:
    pass

def other(c, m, file, type, status, getattrs):
  _, original, caption = getattrs(m=m)
  m.reply_chat_action(t)
  status.edit("**Sending**`...`")
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
    original = getattrs(m, s)
    s.edit_reply_markup(original)
  status.delete()

def music(c, m, status, getattrs):
  url, _, caption = getattrs(m=m)
  m.reply_chat_action(ra)
  audio = YTM(url)
  status.edit("**Sending**`...`")
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)
  status.delete()