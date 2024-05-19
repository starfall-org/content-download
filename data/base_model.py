from datetime import datetime
from hydrogram.enums import ChatType
from pytz import timezone
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .environment import DATABASE_URL

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    update_time = Column(String)
    update_by = Column(String)
    message_count = Column(Integer, default=1)
    first_time = Column(String)
    first_on_chat = Column(String)
    first_with = Column(String)


class Chat(Base):
    __tablename__ = "chats"

    username = Column(String)
    title = Column(String)
    update_time = Column(String)
    update_by = Column(String)
    first_time = Column(String)
    first_with = Column(String)


class Save:
    @staticmethod
    def user(m):
        session = SessionLocal()
        try:
            current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
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

            user = session.query(User).filter(User.user_id == user_id).first()
            if user:
                user.username = username
                user.first_name = first_name
                user.update_time = date
                user.update_by = "Content Download"
                user.message_count += 1
            else:
                user = User(
                    user_id=user_id,
                    username=username,
                    first_name=first_name,
                    update_time=date,
                    update_by="Content Download",
                    first_time=date,
                    first_on_chat=first_on_chat,
                    first_with="Content Download",
                )
                session.add(user)

            session.commit()
        finally:
            session.close()

    @staticmethod
    def chat(m):
        session = SessionLocal()
        try:
            current_time = datetime.now(timezone("Asia/Ho_Chi_Minh"))
            date = current_time.strftime("%d - %B - %Y")
            title = m.chat.title
            username = m.chat.username
            chat_id = str(m.chat.id)

            chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
            if chat:
                chat.username = username
                chat.title = title
                chat.update_time = date
                chat.update_by = "Content Download"
            else:
                chat = Chat(
                    chat_id=chat_id,
                    username=username,
                    title=title,
                    update_time=date,
                    update_by="Content Download",
                    first_time=date,
                    first_with="Content Download",
                )
                session.add(chat)

            session.commit()
        finally:
            session.close()


class Get:
    @staticmethod
    def users_list():
        session = SessionLocal()
        try:
            result = []
            users = session.query(User).all()
            for user in users:
                user_id = user.user_id
                username = user.username
                first_name = user.first_name
                if username is None:
                    result.append(
                        f"<a href='tg://user?id={user_id}'><b>{first_name}</b></a> (ID: <code>{user_id}</code>)"
                    )
                else:
                    result.append(
                        f"<a href='https://t.me/{username}'><b>{first_name}</b></a> (ID: (<code>{user_id}</code>)"
                    )
            return len(result), result
        finally:
            session.close()

    @staticmethod
    def chats_list():
        session = SessionLocal()
        try:
            result = []
            chats = session.query(Chat).all()
            for chat in chats:
                chat_id = chat.chat_id
                username = chat.username
                title = chat.title
                if username is None:
                    result.append(
                        f"<a href='tg://user?id={chat_id}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)"
                    )
                else:
                    result.append(
                        f"<a href='https://t.me/{username}'><b>{title}</b></a> (ID: <code>{chat_id}</code>)"
                    )
            return len(result), result
        finally:
            session.close()

    @staticmethod
    def get_count():
        session = SessionLocal()
        try:
            users_count = session.query(User).count()
            chats_count = session.query(Chat).count()
            return users_count, chats_count
        finally:
            session.close()

    @staticmethod
    def user_history(user_id):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.user_id == str(user_id)).first()
            if user:
                first_time = user.first_time
                on_chat = user.first_on_chat
                on_with = user.first_with
                msg_count = user.message_count
                return first_time, on_chat, on_with, msg_count
        finally:
            session.close()
