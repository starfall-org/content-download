from pyrogram import filters

def filter_owner(_, __, m):
    return m.from_user.id == 5665225938
    
def content_download_channel(_, __, m):
    if m.chat.username == "contentdownload_group":
        if hasattr(m, "sender_chat"):
            return m.sender_chat.username == "contentdownload":
                return False
    
owner = filters.create(filter_owner)
channel_post  = filters.create(content_download_channel)
    