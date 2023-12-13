from utils.secret import deta

#
chats_db = deta.Base("chats")
users_db = deta.Base("users")

#
def save_user(user_id, username, first_name):
  users_db.put({
      "username": username,
      "first_name": first_name
  },
               key=f"{user_id}")
#
def save_chat(chat_id, username, title):
  chats_db.put({"username": username, "title": title}, key=f"{chat_id}")
#
def get_users():
  users = users_db.fetch().items
  result = []
  for user in users:
    user_id = user["key"]
    username = user.get("username")
    first_name = user.get("first_name")
    if username is None:
      result.append(
          f"<a href='tg://user?id={user_id}'><b>{first_name}</b></a> (ID: <code>{user_id}</code>)"
      )
    else:
      result.append(
          f"<a href='https://t.me/{username}'><b>{first_name}</b></a> (ID: (<code>{user_id}</code>)"
      )
  return len(result), result


#
def get_chats():
  chats = chats_db.fetch().items
  result = []
  for chat in chats:
    chat_id = chat["key"]
    username = chat.get("username")
    title = chat.get("title")
    if username is None:
      result.append(
          f"<a href='tg://user?id={chat_id}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)"
      )
    else:
      result.append(
          f"<a href='https://t.me/{username}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)"
      )
  return len(result), result
