from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class PresetContent(SQLModel, table=True):
    __tablename__ = "contentdownload_presets"
    id: int = Field(primary_key=True)
    name: str
    content: str


class Chat(SQLModel, table=True):
    __tablename__ = "contentdownload_chats"
    id: int = Field(primary_key=True)
    username: str | None = Field(default=None)
    title: str
    is_user: bool = Field(default=False)
    is_channel: bool = Field(default=False)
    is_group: bool = Field(default=False)
    is_supergroup: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    is_banned: bool = Field(default=False)
    can_reply: bool = Field(default=True)
    last_active: datetime = Field(default_factory=datetime.now)


class GroupStats(SQLModel, table=True):
    __tablename__ = "contentdownload_groupstats"
    id: int = Field(primary_key=True)
    title: str
    username: str | None
    member_count: list["MemberCount"] = Relationship(back_populates="group")


class MemberCount(SQLModel, table=True):
    __tablename__ = "contentdownload_membercount"
    id: int = Field(primary_key=True)
    count: int
    date: datetime = Field(default_factory=datetime.now)
    group_id: int = Field(foreign_key="contentdownload_groupstats.id")
    group: GroupStats = Relationship(back_populates="member_count")
