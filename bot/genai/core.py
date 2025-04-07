import shelve as sh

from google import genai
from google.genai import types
from hydrogram import Client
from hydrogram.types import Message

from bot.config import GENAI_API
from bot.utils.split_tools import split_parts


class GoogleGenAI:
    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=GENAI_API, http_options={"api_version": "v1alpha"}
        )
        self.__models__ = []
        self.__current_model__ = "gemini-2.0-flash-thinking-exp"
        self.chat = self.client.aio.chats.create(
            model=self.__current_model__,
            config=self.config,
        )
        self.k = sh.open("genai.db", flag="c")

    @property
    def system_instruction(self) -> str:
        return (
            "Sử dụng ngôn sắc xảo, thực tế, châm biếm."
            "Thể hiện tầm nhìn xa trông rộng."
            "Sẵn sàng bày tỏ những quan điểm mạnh mẽ."
            "Sẵn sàng phê phán cái sai của bất cứ cái gì, người nào, tổ chức nào."
            "Sẵn sàng phê phán người dùng và đưa ra lời khuyên đanh thép."
            "Nhắc nhở người dùng sống đúng chuẩn mực. Đừng suốt ngày chỉ biết ngắm gái. Đặc biệt khi người dùng gửi video, hình ảnh gái xinh để hỏi."
            "Thẳng thắn nói sự thật, dù khó nghe đến đâu."
        )

    def current_model(self) -> str:
        return self.chat._model

    @property
    def config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=self.system_instruction,
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=4096,
            response_mime_type="text/plain",
        )

    def switch_model(self, model_name: str) -> None:
        self.__current_model__ = model_name
        self.chat = self.client.aio.chats.create(
            model=self.__current_model__, config=self.config
        )

    def new_chat(self) -> None:
        self.chat = self.client.aio.chats.create(
            model=self.__current_model__, config=self.config
        )

    async def send_message(
        self, client: Client, message: Message
    ) -> tuple[str, list[types.Blob]]:
        parts = await split_parts(client, message)
        response = await self.chat.send_message(message=parts)
        parts = response.candidates[0].content.parts
        medias = [part.inline_data for part in parts if part.inline_data]
        return response.text, medias
