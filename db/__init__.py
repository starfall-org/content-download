from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hydrogram.types import Message
from hydrogram.enums import ChatType
from hydrogram import DATABASE_URL
from asyncer import asyncify
from .models import Base, User, Chat


class Database:
    def __init__(self):
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def user_obj(self, m: Message, is_blocked: bool = False):
        return User(
            id=m.from_user.id,
            username=m.from_user.username,
            first_name=m.from_user.first_name,
            last_name=m.from_user.last_name,
            is_blocked=is_blocked,
            last_active=m.date,
        )

    def chat_obj(self, m: Message, is_banned: bool = False):
        return Chat(
            id=m.chat.id,
            username=m.chat.username,
            title=m.chat.title,
            is_banned=is_banned,
            last_active=m.date,
        )

    def get_user(self, user_id: int):
        return self.session.query(User).filter_by(id=user_id).first()

    def get_chat(self, chat_id: int):
        return self.session.query(Chat).filter_by(id=chat_id).first()

    def save(self, m: Message):
        user = self.user_obj(m)
        if m.chat.type != ChatType.PRIVATE:
            chat = self.chat_obj(m)
            self.session.merge(chat)
        self.session.merge(user)
        self.session.commit()

    def set_status(
        self, m: Message, is_banned: bool | None = False, is_blocked: bool | None = None
    ):
        if is_banned:
            chat = self.chat_obj(m, is_banned)
            self.session.merge(chat)
        if is_blocked:
            user = self.user_obj(m, is_blocked)
            self.session.merge(user)
        self.session.commit()

    def users_count(self):
        return self.session.query(User).count()

    def chats_count(self):
        return self.session.query(Chat).count()


async def save(
    m: Message, is_banned: bool | None = None, is_blocked: bool | None = None
):
    def backgroud():
        db = Database()
        if is_banned or is_blocked:
            db.set_status(m, is_banned, is_blocked)
        else:
            db.save(m)
        db.session.close()

    Thread(target=backgroud).start()


async def count():
    def func():
        db = Database()
        users = db.users_count()
        chats = db.chats_count()
        return users, chats

    result = await asyncify(func)()
