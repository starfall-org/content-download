from init import mongo
from datetime import datetime
from pytz import timezone
from hydrogram.types import ChatTypes

chats = mongo["chats"]
users = mongo["users"]

class Save:
    @staticmethod
    def user(m):
        current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
        date = current_time.strftime("%d - %B - %Y")
        if m.chat.username:
            first_on_chat = f"{m.chat.title}({m.chat.username}) - {m.chat.id}"
        else:
            first_on_chat = f"{m.chat.title} - {m.chat.id}"
        if m.chat.type == ChatTypes.PRIVATE:
            first_on_chat = "Private Chat"
        first_name = m.user.first_name
        username = m.user.username
        user_id = str(m.user.id)
        update = users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "username": username,
                    "first_name": first_name,
                    "update": date,
                    "update_by": "Content Download"
                },
                "$setOnInsert": {
                    "first_time": date,
                    "first_on_chat": first_on_chat,
                    "first_with": "TikTok & Douyin"
                }
            },
            upsert=True
        )
        print(update)
        
    @staticmethod
    def chat(m):
        current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
        date = current_time.strftime("%d - %B - %Y")
        title = m.chat.title
        username = m.chat.username
        chat_id = m.chat.id
        update = chats.update_one(
            {"_id": chat_id},
            {
                "$set": {
                    "username": username,
                    "title": title,
                    "update": date,
                    "update_by": "TikTok & Douyin"
                },
                "$setOnInsert": {
                    "first_time": date,
                    "first_with": "TikTok & Douyin"
                }
            },
            upsert=True
        )
        print(update)
        

class Get:
    @staticmethod
    def users_list():
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
    
    @staticmethod
    def chats_list():
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
    
    @staticmethod
    def get_count():
        users_count = users.count_documents({})
        chats_count = chats.count_documents({})
        return users_count, chats_count