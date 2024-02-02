from .environ import pg
from datetime import datetime
from pytz import timezone
from hydrogram.enums import ChatType

class Save:
    @staticmethod
    def user(m):
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
        
        with pg.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (_id, username, first_name, update_time, update_by, message_count, first_time, first_on_chat, first_with)
                VALUES (%s, %s, %s, %s, %s, 1, %s, %s, %s)
                ON CONFLICT (_id) DO UPDATE 
                SET 
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    update_time = EXCLUDED.update_time,
                    update_by = EXCLUDED.update_by,
                    message_count = users.message_count + 1
            """, (user_id, username, first_name, date, "Content Download", date, first_on_chat, "Content Download"))
        
    @staticmethod
    def chat(m):
        current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
        date = current_time.strftime("%d - %B - %Y")
        title = m.chat.title
        username = m.chat.username
        chat_id = str(m.chat.id)
        
        with pg.cursor() as cursor:
            cursor.execute("""
                INSERT INTO chats (_id, username, title, update_time, update_by)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (_id) DO UPDATE 
                SET 
                    username = EXCLUDED.username,
                    title = EXCLUDED.title,
                    update_time = EXCLUDED.update_time,
                    update_by = EXCLUDED.update_by
            """, (chat_id, username, title, date, "Content Download"))

class Get:
    @staticmethod
    def users_list():
        with pg.cursor() as cursor:
            cursor.execute("SELECT _id, username, first_name FROM users")
            result = cursor.fetchall()
            
        formatted_result = [
            f"<a href='tg://user?id={row[0]}'><b>{row[2]}</b></a> (ID: <code>{row[0]}</code>)" if row[1] is None
            else f"<a href='https://t.me/{row[1]}'><b>{row[2]}</b></a> (ID: <code>{row[0]}</code>)"
            for row in result
        ]
        
        return len(formatted_result), formatted_result

    @staticmethod
    def chats_list():
        with pg.cursor() as cursor:
            cursor.execute("SELECT _id, username, title FROM chats")
            result = cursor.fetchall()
            
        formatted_result = [
            f"<a href='tg://user?id={row[0]}'><b>{row[2]}</b></a> (ID: <code>{row[0]}</code>)" if row[1] is None
            else f"<a href='https://t.me/{row[1]}'><b>{row[2]}</b></a> (ID: <code>{row[0]}</code>)"
            for row in result
        ]
        
        return len(formatted_result), formatted_result

    @staticmethod
    def get_count():
        with pg.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM chats")
            chats_count = cursor.fetchone()[0]
            
        return users_count, chats_count

    @staticmethod
    def user_history(user_id):
        with pg.cursor() as cursor:
            cursor.execute("SELECT first_time, first_on_chat, first_with, message_count FROM users WHERE _id = %s", (str(user_id),))
            data = cursor.fetchone()

        first_time, on_chat, on_with, msg_count = data if data else (None, None, None, None)
        return first_time, on_chat, on_with, msg_count