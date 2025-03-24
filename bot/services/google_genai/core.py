from google import genai
from google.genai import types
from hydrogram import Client
from hydrogram.types import Message

from bot.config import GENAI_API
from bot.utils.split_tools import split_parts


class GoogleGenAI:
    def __init__(self):
        self.client = genai.Client(api_key=GENAI_API)
        self.__models__ = []
        self.__current_model__ = "gemini-2.0-flash"
        self.chat = self.client.aio.chats.create(
            model=self.__current_model__,
            config=self.config,
        )

    @property
    def system_instruction(self):
        return "You are a helpful assistant. Answer in Vietnamese by default."

    @property
    def models(self):
        self.__models__ = [model for model in self.client.models.list()]
        return self.__models__

    @property
    def config(self):
        return types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=4096,
            response_mime_type="text/plain",
        )

    def switch_model(self, model_name: str):
        self.__current_model__ = model_name
        return self.client.aio.chats.create(
            model=self.__current_model__, config=self.config
        )

    def new_chat(self):
        self.chat = self.client.aio.chats.create(
            model=self.__current_model__, config=self.config
        )

    async def send_message(self, client: Client, message: Message):
        parts = await split_parts(client, message)
        return await self.chat.send_message(message=parts)
