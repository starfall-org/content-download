from asyncio import to_thread

from hydrogram import DATABASE_URL
from hydrogram.enums import ChatType
from sqlmodel import Session, SQLModel, create_engine, select

from utils.models import ChatArgs

from .models import Chat, PresetContent


class Database:
    def __init__(self):
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        SQLModel.metadata.create_all(engine)
        self.session = Session(engine)

    def __get_chat__(self, chat_id: int):
        return self.session.exec(select(Chat).where(Chat.id == chat_id)).first()

    def __update_chat__(self, args: ChatArgs):
        chat = Chat(
            id=args.message.chat.id,
            title=args.message.chat.title,
            username=args.message.chat.username,
            is_admin=args.is_admin,
            is_banned=args.is_banned,
            can_reply=args.can_reply,
            is_channel=args.is_channel,
            is_group=args.is_group,
            is_supergroup=args.is_supergroup,
        )
        self.session.add(chat)
        self.session.commit()

    def __count_chat__(self):
        return len(self.session.exec(select(Chat)).all())

    def __get_preset__(self, name: str):
        return self.session.exec(
            select(PresetContent).where(PresetContent.name == name)
        ).first()

    def __add_preset__(self, name: str, content: str):
        preset = PresetContent(name=name, content=content)
        self.session.add(preset)
        self.session.commit()

    @staticmethod
    async def update_chat(args: ChatArgs):
        args.is_admin = (
            args.message.from_user
            and args.message.from_user.id in args.get_administrators()
        )
        args.is_channel = args.message.chat.type == ChatType.CHANNEL
        args.is_group = args.message.chat.type == ChatType.GROUP
        args.is_supergroup = args.message.chat.type == ChatType.SUPERGROUP
        return await to_thread(Database().__update_chat__, args)

    @staticmethod
    async def get_chat(chat_id: int):
        return await to_thread(Database().__get_chat__, chat_id)

    @staticmethod
    async def count_chat():
        return await to_thread(Database().__count_chat__)

    @staticmethod
    async def get_preset(name: str):
        return await to_thread(Database().__get_preset__, name)

    @staticmethod
    async def add_preset(name: str, content: str):
        return await to_thread(Database().__add_preset__, name, content)
