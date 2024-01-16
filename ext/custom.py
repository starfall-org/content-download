from pyrogram import filters

def filter_owner(_, __, m):
    return m.from_user.id == 5665225938
    
def content_download_channel(_, __, m):
    return (m.sender_chat.username != "contentdownload" and m.chat.username == "contentdownload_group")
    
owner = filters.create(filter_owner)
channel_post  = filters.create(content_download_channel)
    