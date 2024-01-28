from library import filters
from data import check_listoff
from library.enums import ChatMemberStatus

def filter_owner(_, __, m):
    return m.from_user.id == 5665225938 if m.from_user else m.sender_chat.username == "contentdownload"
    
def content_download_channel(_, __, m):
    return not m.sender_chat.username == "contentdownload" if m.sender_chat and m.forward_from_chat and m.chat.username == "contentdownload_group" else True

def check_listoff_filter(_, __, m):
    return not check_listoff(m.chat.id)
    
def filter_group_admin(_, __, m):
    if m.from_user:
        user_status = m.chat.get_member(m.from_user.id).status
        return user_status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]
    return False
    
owner = filters.create(filter_owner)
channel_post  = filters.create(content_download_channel)
filter_on = filters.create(check_listoff_filter)
filter_right = filters.create(filter_group_admin)