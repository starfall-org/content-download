from sqlalchemy import Column, String, BigInteger, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    is_blocked = Column(Boolean, default=False)
    last_active = Column(DateTime)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    title = Column(String)
    is_banned = Column(Boolean, default=False)
    last_active = Column(DateTime)
