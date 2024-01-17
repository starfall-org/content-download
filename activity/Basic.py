from pyrogram.enums import ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from ext import save
from init import collection

typing = ChatAction.TYPING
button = InlineKeyboardMarkup([[
        InlineKeyboardButton("Youtube",url="https://youtube.com/@DouyinShare"), InlineKeyboardButton("Collection", url=collection)],[
        InlineKeyboardButton("Group",url="https://t.me/contentdownload_group"),
        InlineKeyboardButton("Channel", url="https://t.me/contentdownload")]])

start_vn = '''__--**Content Download bot**--__ cho phép bạn tải nội dung từ nhiều nguồn khác nhau trên mạng xã hội. 
Bạn có thể tải video, hình ảnh, âm thanh, hoặc tệp từ các trang web như __Youtube__, __TikTok/Douyin__, __Facebook__, __Twitter__, và nhiều trang web khác.'''
start_en = '''__--**Content Download bot**--__ allows you to download content from various sources on social media. 
You can download videos, images, audio, or file from websites such as __Youtube__, __TikTok/Douyin__, __Facebook__, __Twitter__, and many more.'''

@Client.on_message(filters.command(["start","help"]) & (filters.private|filters.chat(-1001832458549)))
def reply_start(c, m):
    save(m)
    m.reply_chat_action(typing)
    language = m.from_user.language_code
    if language == "vi":
        msg = start_vn
    else:
        msg = start_en
    m.reply(msg, reply_markup=button)