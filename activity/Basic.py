from pyrogram import filters, Client
from ext.util import save
from ext.var import button, t

start_vn = '''**Content Download bot** cho phép bạn tải nội dung từ nhiều nguồn khác nhau trên mạng xã hội. 
Bạn có thể tải video, hình ảnh, âm thanh, hoặc tệp từ các trang web như Youtube, TikTok/Douyin, Facebook, Twitter, và nhiều trang web khác. 

Dùng lệnh /help để biết thêm chi tiết.'''
start_en = '''**Content Download bot** allows you to download content from various sources on social media. 
You can download videos, images, audio, or file from websites such as Youtube, TikTok/Douyin, Facebook, Twitter, and many more. 

Send /help command for more details.'''

@Client.on_message(filters.command("start") & (filters.private|filters.chat(-1001832458549)))
def handle_start(c, m):
  save(m)
  m.reply_chat_action(t)
  lan = m.from_user.language_code
  if lan == "vi":
    msg = start_vn
  else:
    msg = start_en
  m.reply(msg, reply_markup=button)

help_vn = ''' **Hướng dẫn:**

`URL chia sẻ:` Tải nội dung từ URL
`/music + URL:` Tải nội dung âm thanh từ URL
`/upload:` Đăng tải tệp lên đám mây từ tin nhắn và nhận liên kết chia sẻ
`/cloud:` Nền tảng lưu trữ'''
help_en = '''**Instructions:**

`Share URL:` Download content from URL
`/music + URL:` Download music content from URL
`/upload:` Upload file to cloud from message and get shareable link
`/cloud:` Storage platform'''

@Client.on_message(filters.command('help') & (filters.private | filters.mentioned))
def handle_help(c, m):
  save(m)
  m.reply_chat_action(t)
  lan = m.from_user.language_code
  if lan == "vi":
    msg = help_vn
  else:
    msg = help_en
  m.reply(msg, reply_markup=button)
