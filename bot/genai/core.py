import shelve as sh

from google import genai
from google.genai import types
from hydrogram.enums import ChatType
from hydrogram.types import Message

from bot.config import GENAI_API
from .config import INSTRUCTIONS

from .chat import GenAIChat


class GoogleGenAI:
    def __init__(self) -> None:
        self.client = genai.Client(
            api_key=GENAI_API, http_options={"api_version": "v1alpha"}
        )
        self.__current_model__ = "gemini-2.0-flash-thinking-exp"
        self.k = sh.open("genai.db", flag="c")
        self.default_instruction = INSTRUCTIONS["FRANKLY"]
        self.__managed_chat__ = self.client.aio.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=f"Danh sách các nhân cách: {INSTRUCTIONS}. Sử dụng change_personality('tên nhân cách') để thay đổi nhân cách.",
                temperature=1,
                top_p=0.95,
                top_k=40,
                max_output_tokens=4096,
                response_mime_type="text/plain",
                tools=[
                    self.change_personality,
                    self.set_instruction,
                    self.get_instruction,
                    self.switch_model,
                    self.list_models,
                    self.current_model,
                ],
            ),
        )

    def get_instruction(self, add: str = "") -> str:
        return (
            self.k.get("system_instruction", default=self.default_instruction)
            + f"\n\n{add}"
        )

    def change_personality(self, personality: str):
        if personality not in INSTRUCTIONS.keys():
            return "Invalid Personality"
        self.default_instruction = INSTRUCTIONS[personality]
        return "Personality Changed"

    def set_instruction(self, text: str | None = None):
        if text:
            self.k["system_instruction"] = text
        else:
            del self.k["system_instruction"]

    def get_config(
        self, additional_system_instruction: str = ""
    ) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=self.get_instruction(additional_system_instruction),
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=4096,
            response_mime_type="text/plain",
        )

    def current_model(self) -> str:
        return self.chat._model

    def list_models(self) -> list[str]:
        models = self.client.models.list()
        return [model.name.split("/")[-1] for model in models]

    def switch_model(self, model_name: str) -> None:
        self.__current_model__ = model_name

    def get_chat(self, m: Message) -> GenAIChat:
        return self.k.get(f"chat_{m.chat.id}") or self.new_chat(m)

    def new_chat(self, m: Message) -> GenAIChat:
        if m.chat.type == ChatType.PRIVATE:
            config = self.get_config(
                f"Bạn đang ở kênh chat riêng tư với người dùng {m.chat.full_name} (ID: {m.chat.id})"
            )
        chat = self.client.aio.chats.create(model=self.__current_model__, config=config)
        genai_chat = GenAIChat(chat)
        self.k[f"chat_{m.chat.id}"] = genai_chat
        return genai_chat

    def get_chats(self) -> list[GenAIChat]:
        return [key for key in self.k.keys() if key.startswith("chat_")]

    def get_managed_chat(self) -> GenAIChat:
        return GenAIChat(self.__managed_chat__)
