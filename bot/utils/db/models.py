from sqlalchemy import Column, String, BigInteger, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
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
    chat_id = Column(BigInteger, primary_key=True)
    username = Column(String)
    title = Column(String)
    update_time = Column(String)
    update_by = Column(String)
    first_time = Column(String)
    first_with = Column(String)
