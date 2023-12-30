from pyrogram.types import InputMediaVideo, InputMediaAudio, InputMediaPhoto, InputMediaDocument
from api_callback.Youtube import YTDL,YTM, ODL
from etc.var import t, rv, ra, sv, sp, sm

def youtube(c, m, s, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  file = YTDL(url)
  m.reply_chat_action(sv)
  s.edit("**Sending**`...`")
  s.edit_media(InputMediaVideo(file))
  s.edit_caption(caption=caption, reply_markup=original)
  original = getattrs(m, s)
  s.edit_reply_markup(original)

def other(c, m, file, type, s, getattrs):
  _, original, caption = getattrs(m=m)
  m.reply_chat_action(t)
  s.edit("**Sending**`...`")
  s = None
  if type == "image":
    m.reply_chat_action(sp)
    s.edit_media(InputMediaPhoto(file))
    s.edit_caption(caption=caption, reply_markup=original)
  elif type == "video":
    m.reply_chat_action(sv)
    s.edit_media(InputMediaVideo(file))
    s.edit_caption(caption=caption, reply_markup=original)
  elif type == "audio":
    m.reply_chat_action(sm)
    s.edit_media(InputMediaAudio(file), caption=caption)
  else:
    return
  original = getattrs(m, s)
  s.edit_reply_markup(original)

def music(c, m, s, getattrs):
  url, _, caption = getattrs(m=m)
  m.reply_chat_action(ra)
  audio = YTM(url)
  s.edit("**Sending**`...`")
  m.reply_chat_action(sm)
  s.edit_media(InputMediaAudio(audio), caption=caption)