from api import YTDL,YTM, ODL
from ext.var import t, rv, ra, sv, sp, sm, sd

def youtube(c, m, getattrs):
  url, original, caption = getattrs(m)
  m.reply_chat_action(rv)
  file = YTDL(url)
  m.reply_chat_action(sv)
  m.reply_video(file, caption=caption, reply_markup=original)
  
def other(c, m, file, tp, getattrs):
  _, original, caption = getattrs(m)
  if type == "image":
    m.reply_chat_action(sp)
    m.reply_photo(file, caption=caption, reply_markup=original)
  elif type == "video":
    m.reply_chat_action(sv)
    m.reply_video(file, caption=caption, reply_markup=original)
  elif type == "audio":
    m.reply_chat_action(sm)
    m.reply_audio(file, caption=caption)
  else:
    m.reply_chat_action(sd)
    m.reply_document(file, reply_markup=original, caption=caption)

def music(c, m, getattrs):
  url, _, caption = getattrs(m)
  m.reply_chat_action(ra)
  audio = YTM(url)
  m.reply_chat_action(sm)
  m.reply_audio(audio, caption=caption)