from .environ import pg
from datetime import datetime
from pytz import timezone
from hydrogram.enums import ChatType

cursor = pg.cursor()

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
        user_id = m.from_user.id
        update = cursor.execute("""
            INSERT INTO users (user_id, username, first_name, update_time, update_by, message_count, first_time, first_on_chat, first_with)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                update_time = EXCLUDED.update_time,
                update_by = EXCLUDED.update_by,
                message_count = users.message_count + EXCLUDED.message_count
        """, (user_id, username, first_name, date, 'Content Download', 1, date, first_on_chat, 'Content Download'))
        pg.commit()
        print(update)

    @staticmethod
    def chat(m):
        current_time = datetime.now(timezone('Asia/Ho_Chi_Minh'))
        date = current_time.strftime("%d - %B - %Y")
        title = m.chat.title
        username = m.chat.username
        chat_id = m.chat.id
        update = cursor.execute("""
            INSERT INTO chats (chat_id, username, title, update_time, update_by, first_time, first_with)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (chat_id) DO UPDATE SET
                username = EXCLUDED.username,
                title = EXCLUDED.title,
                update_time = EXCLUDED.update_time,
                update_by = EXCLUDED.update_by
        """, (chat_id, username, title, date, 'Content Download', date, 'Content Download'))
        pg.commit()
        print(update)