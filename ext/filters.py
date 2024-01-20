from hydrogram import filters

def filter_owner(_, __, m):
    return m.from_user.id == 5665225938 if m.from_user else m.sender_chat.username == "contentdownload"
    
def content_download_channel(_, __, m):
    return not m.sender_chat.username == "contentdownload" if m.sender_chat and m.forward_from_chat and m.chat.username == "contentdownload_group" else True
    
owner = filters.create(filter_owner)
channel_post  = filters.create(content_download_channel)