from datetime import datetime
from sqlalchemy import String, BigInteger, Boolean, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: int = mapped_column(BigInteger, primary_key=True)
    username: str | None = mapped_column(String, nullable=True)
    first_name: str = mapped_column(String)
    last_name: str | None = mapped_column(String, nullable=True)
    is_blocked: bool = mapped_column(Boolean, default=False)
    last_active: datetime = mapped_column(DateTime)


class Chat(Base):
    __tablename__ = "chats"
    id: int = mapped_column(BigInteger, primary_key=True)
    username: str | None = mapped_column(String, nullable=True)
    title: str = mapped_column(String)
    is_banned: bool = mapped_column(Boolean, default=False)
    last_active: datetime = mapped_column(DateTime)
