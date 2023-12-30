from api_callback.Youtube import YTDL,YTM, ODL
from etc.var import t, rv, ra, sv, sp, sm

def youtube(c, m, stt, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  file = YTDL(url)
  m.reply_chat_action(sv)
  stt.edit("**Sending**`...`")
  sf = m.reply_video(file, caption=caption, reply_markup=original)
  original = getattrs(m, sf)
  sf.edit_reply_markup(original)

def other(c, m, file, tp, stt, getattrs):
  _, original, caption = getattrs(m=m)
  m.reply_chat_action(t)
  stt.edit("**Sending**`...`")
  sf = None
  if type == "image":
    m.reply_chat_action(sp)
    sf = m.reply_photo(file, caption=caption, reply_markup=original)
  elif type == "video":
    m.reply_chat_action(sv)
    sf = m.reply_video(file, caption=caption, reply_markup=original)
  elif type == "audio":
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
  if sf:
    original = getattrs(m, sf)
    sf.edit_reply_markup(original)

def music(c, m, stt, getattrs):
  url, _, caption = getattrs(m=m)
  m.reply_chat_action(ra)
  audio = YTM(url)
  stt.edit("**Sending**`...`")
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)