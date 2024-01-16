from pyrogram import filters

def filter_owner(_, __, m):
    return m.from_user.id == 5665225938
    
owner = filters.create(filter_owner)
    