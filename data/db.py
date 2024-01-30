from init import mongo

#
chats = mongo["chats"]
users = mongo["users"]

#
def save_user(user_id, username, first_name):
    update = users.update_one(str(user_id), {"username": username,
        "first_name": first_name}, upsert=True)
    print(update)
#
def save_chat(chat_id, username, title):
    update = chats.update_one(str(chat_id), {"username": username, "title": title}, 
        upsert=True)
#
def get_users():
    result = []
    for user in users.find():
        user_id = user["_id"]
        username = user["username"]
        first_name = user["first_name"]
        if username is None:
            result.append(
                f"<a href='tg://user?id={user_id}'><b>{first_name}</b></a> (ID: <code>{user_id}</code>)")
        else:
            result.append(
                f"<a href='https://t.me/{username}'><b>{first_name}</b></a> (ID: (<code>{user_id}</code>)")
    return len(result), result


#
def get_chats():
    result = []
    for chat in chats.find():
        chat_id = chat["_id"]
        username = chat["username"]
        title = chat["title"]
        if username is None:
            result.append(
                f"<a href='tg://user?id={chat_id}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)")
        else:
            result.append(
                f"<a href='https://t.me/{username}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)")
    return len(result), result