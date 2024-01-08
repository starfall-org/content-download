from pyrogram import Client, filters
from data.secret import webstream
from ext.var import t
import os, time 

@Client.on_message(filters.command('stream'))
def stream(c,m):
  m.reply_chat_action(t)
  if m.reply_to_message:
    reply_to = m.reply_to_message
    box = reply_to.chat.id
    mid = reply_to.id
    if reply_to.video:
      file_id = reply_to.video.file_id
      file_type = 'video'
    elif reply_to.audio:
      file_id = reply_to.audio.file_id
      file_type = 'audio'
    elif reply_to.photo:
      file_id = reply_to.photo.file_id
      file_type = 'photo'
  else:
    box = m.chat.id
    mid = m.id
    if m.video:
      file_id = m.video.file_id
      file_type = 'video'
    elif m.audio:
      file_id = m.audio.file_id
      file_type = 'audio'
    elif m.photo:
      file_id = m.photo.file_id
      file_type = 'photo'
    else:
      m.reply('Không phát hiện đối tượng có thể stream, vui lòng cung cấp thêm.', quote=True)
      return
  main_stream = f'{webstream}/stream?box={box}&id={mid}'
  m.reply(f'Liên kết Stream:\n{main_stream}', quote=True)
  
@Client.on_message(filters.command('setstream'))
def set_webstream(c,m):
  url = m.command[1]
  os.environ['WEBSTREAM'] = url
  st = m.reply(f'Đã cập nhật stream url thành {url}', quote=True)
  time.sleep(10)
  st.delete()
  m.delete()