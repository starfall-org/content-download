from api_callback.Youtube import YTDL,YTM, ODL
from etc.var import t, rv, ra, sv, sp, sm

def youtube(c, m, s, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  file = YTDL(url)
  m.reply_chat_action(sv)
  s.edit("**Sending**`...`")
  st = m.reply_video(file, caption=caption, reply_markup=original)
  original = getattrs(m, st)
  st.edit_reply_markup(original)

def other(c, m, file, type, s, getattrs):
  _, original, caption = getattrs(m=m)
  m.reply_chat_action(t)
  s.edit("**Sending**`...`")
  st = None
  if type == "image":
    m.reply_chat_action(sp)
    st = m.reply_photo(file, caption=caption, reply_markup=original)
  elif type == "video":
    m.reply_chat_action(sv)
    st = m.reply_video(file, caption=caption, reply_markup=original)
  elif type == "audio":
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
  if st:
    original = getattrs(m, st)
    st.edit_reply_markup(original)

def music(c, m, s, getattrs):
  url, _, caption = getattrs(m=m)
  m.reply_chat_action(ra)
  audio = YTM(url)
  s.edit("**Sending**`...`")
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)