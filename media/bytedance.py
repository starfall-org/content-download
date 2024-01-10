from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.bytedance import TDDL
from ext.util import send_videos, send_photos, send_audios, get_share_links
from ext.upload import upload
from ext.var import sv, rv, ra, sm
import logging

def tiktokuserlink(c, m, url, caption):
  original = InlineKeyboardMarkup([[InlineKeyboardButton("TikTok User",
                                                         url=url)]])
  share_links = get_share_links(url)
  list_video = []
  list_file = []
  list_photo = []
  list_music = []
  list_music_url = []
  for sharelink in share_links:
    file, link, is_video, music = TDDL(sharelink)
    if is_video == True:
      list_video.append(link)
      list_file.append(file)
    else:
      list_photo.extend(link)
    if music:
      list_music.append(music[0])
      list_music_url.append(music[1])
  if list_photo:
    try:
      send_photos(m, list_photo, original, caption)
    except Exception as e:
      logging.error(e)
  if list_video:
    try:
      send_videos(m, list_video, original, caption)
    except:
      send_videos(m, list_file, original, caption)
  if list_music:
      try:
          send_audios(m, list_music_url, caption)
      except:
          send_audios(m, list_music, caption)
  
def tikdou(c, m, getattrs):
  url, original, caption = getattrs(m=m)
  m.reply_chat_action(rv)
  try:
    file, link, is_video, music = TDDL(url)
  except:
    tiktokuserlink(c, m, url, caption)
    return
  if is_video == False:
    try:
        send_photos(m, link, original, caption)
    except:
        send_photos(m, file, original, caption)
    if music:
        try:
            send_audios(m, [music[1]], caption)
        except:
            send_audios(m, [music[0]], caption)
  elif is_video == True:
    m.reply_chat_action(sv)
    try:
      st = m.reply_video(link, caption=caption, reply_markup=original)
    except:
      st = m.reply_video(file, caption=caption, reply_markup=original)
    original = getattrs(m, st) 
    st.edit_reply_markup(original)
    if m.chat.username == "contentdownload":
      upload(file)
      
def tdmusic(c, m, getattrs):
  url, _, caption = getattrs(m=m)
  m.reply_chat_action(ra)
  _, __, ____, audio = TDDL(url)
  m.reply_chat_action(sm)
  try:
      m.reply_audio(audio[1], caption=caption)
  except:
      m.reply_audio(audio[0], caption=caption)