from .environ import pg
from datetime import datetime
from pytz import timezone
from hydrogram.enums import ChatType

class Save:
    @staticmethod
    def user(m):
        conn, cursor = pg()
        current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
        date = current_time.strftime("%d - %m - %Y")
        if m.chat.username:
            first_on_chat = f"{m.chat.title}({m.chat.username}) - {m.chat.id}"
        else:
            first_on_chat = f"{m.chat.title} - {m.chat.id}"
        if m.chat.type == ChatType.PRIVATE:
            first_on_chat = "Private Chat"
        first_name = m.from_user.first_name
        username = m.from_user.username
        user_id = str(m.from_user.id)
        
        cursor.execute("""
            INSERT INTO users (user_id, username, first_name, update_time, update_by, message_count, first_time, first_on_chat, first_with)
            VALUES (%s, %s, %s, %s, %s, 1, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE 
            SET 
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                update_time = EXCLUDED.update_time,
                update_by = EXCLUDED.update_by,
                message_count = users.message_count + 1
        """, (user_id, username, first_name, date, "Content Download", date, first_on_chat, "Content Download"))
        
        conn.commit()
        
        
    @staticmethod
    def chat(m):
        conn, cursor = pg()
        current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
        date = current_time.strftime("%d - %B - %Y")
        title = m.chat.title
        username = m.chat.username
        chat_id = str(m.chat.id)
        
        cursor.execute("""
            INSERT INTO chats (chat_id, username, title, update_time, update_by, first_time, first_with)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (chat_id) DO UPDATE 
            SET 
                username = EXCLUDED.username,
                title = EXCLUDED.title,
                update_time = EXCLUDED.update_time,
                update_by = EXCLUDED.update_by
        """, (chat_id, username, title, date, "Content Download", date, "Content Download"))
        
        conn.commit()

class Get:
    @staticmethod
    def users_list():
        conn, cursor = pg()
        result = []
        cursor.execute("SELECT * FROM users")
        for user in cursor.fetchall():
            user_id = user[0]
            username = user[1]
            first_name = user[2]
            if username is None:
                result.append(
                    f"<a href='tg://user?id={user_id}'><b>{first_name}</b></a> (ID: <code>{user_id}</code>)")
            else:
                result.append(
                    f"<a href='https://t.me/{username}'><b>{first_name}</b></a> (ID: (<code>{user_id}</code>)")
        return len(result), result
    
    @staticmethod
    def chats_list():
        conn, cursor = pg()
        result = []
        cursor.execute("SELECT * FROM chats")
        for chat in cursor.fetchall():
            chat_id = chat[0]
            username = chat[1]
            title = chat[2]
            if username is None:
                result.append(
                    f"<a href='tg://user?id={chat_id}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)")
            else:
                result.append(
                    f"<a href='https://t.me/{username}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)")
        return len(result), result
    
    @staticmethod
    def get_count():
        conn, cursor = pg()
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM chats")
        chats_count = cursor.fetchone()[0]
        return users_count, chats_count
        
    @staticmethod
    def user_history(user_id):
        conn, cursor = pg()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (str(user_id),))
        data = cursor.fetchone()
        if data:
            first_time = data[6]
            on_chat = data[7]
            on_with = data[8]
            msg_count = data[5]
            return first_time, on_chat, on_with, msg_count