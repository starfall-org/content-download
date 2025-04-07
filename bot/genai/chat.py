import io

from google.genai import chats
from hydrogram import Client
from hydrogram.types import Message

from bot.schemas.media import Media
from bot.utils.split_tools import split_parts


class GenAIChat:
    def __init__(self, chat: chats.AsyncChat):
        self.chat = chat

    async def send(
        self, client: Client, message: Message
    ) -> tuple[str | None, Media | None]:
        parts = await split_parts(client, message)
        response = await self.chat.send_message(message=parts)
        media = None
        if candidates := response.candidates:
            if parts := candidates[0].content.parts:
                if inline_data := parts[0].inline_data:
                    media = Media(
                        data=io.BytesIO(inline_data.data),
                        mime_type=inline_data.mime_type,
                    )
        return response.text, media
