from pyrogram.types import InputMediaPhoto, InputMediaVideo
from typing import List
from utils.vả import sp, sv
from utils.db import save_chat, save_user
from utils.upld import upload_file
import requests, threading, os


def save(m):
  if str(m.chat.id).startswith("-100"):
    chat_thread = threading.Thread(target=save_chat,
                                   args=(m.chat.id, m.chat.username,
                                         m.chat.title))
    chat_thread.start()

  if m.from_user:
    user_thread = threading.Thread(target=save_user,
                                   args=(m.from_user.id, m.from_user.username,
                                         m.from_user.first_name))
    user_thread.start()
    os.system(f"echo User: {m.from_user.first_name} ({m.from_user.id}) \nChat: {m.chat.title} ({m.chat.id})")


#
def uploads(file):
  uf = threading.Thread(target=upload_file, args=(file, ))
  uf.start()


#
def send_photos(m, c, button, photo_links: List[str], caption):
  m.reply_chat_action(sp)
  if len(photo_links) == 1:
    for link in photo_links:
      m.reply_photo(link, reply_markup=button, caption=caption)
  else:
    for i in range(0, len(photo_links) - 1, 10):
      media_group = [
          InputMediaPhoto(link)
          for link in photo_links[i:min(i + 10,
                                        len(photo_links) - 1)]
      ]
      m.reply_chat_action(sp)
      m.reply_media_group(media_group)
    m.reply_chat_action(sp)
    m.reply_photo(photo_links[-1], caption=caption, reply_markup=button)


#
def send_videos(m, c, button, video_links: List[str], caption):
  m.reply_chat_action(sv)
  if len(video_links) == 1:
    for link in video_links:
      m.reply_video(link, reply_markup=button, caption=caption)
  else:
    for i in range(0, len(video_links) - 1, 10):
      media_group = [
          InputMediaVideo(link)
          for link in video_links[i:min(i + 10,
                                        len(video_links) - 1)]
      ]
      m.reply_chat_action(sv)
      m.reply_media_group(media_group)
    m.reply_chat_action(sp)
    m.reply_video(video_links[-1], caption=caption, reply_markup=button)


#
def server_info():
  try:
    response = requests.get('https://ipinfo.io')
    data = response.json()
    ip = data.get('ip', 'N/A')
    city = data.get('city', 'N/A')
    region = data.get('region', 'N/A')
    country = data.get('country', 'N/A')
    provider = data.get('org', 'N/A')

    server_info = f"IP: {ip}\nCity: {city}\nRegion: {region}\nCountry: {country}\nProvider: {provider}"

  except Exception as e:
    server_info = f"Error: {e}"

  return server_info
