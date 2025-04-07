import io

from google.genai import chats, types
from hydrogram import Client
from hydrogram.types import Message

from bot.schemas.media import Media
from bot.utils.split_tools import split_parts


class GenAIChat:
    def __init__(self, chat: chats.AsyncChat):
        self.chat = chat

    async def send(self, client: Client, message: Message) -> tuple[str, types.Blob]:
        parts = await split_parts(client, message)
        response = await self.chat.send_message(message=parts)
        parts = response.candidates[0].content.parts
        if media := parts[0].inline_data:
            media_io = io.BytesIO(media.data)
            media_io.name = "media." + media.mime_type.split("/")[-1]
            media = Media(
                data=media_io,
                mime_type=media.mime_type,
            )
        else:
            media = None
        return (response.text, media)
