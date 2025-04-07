import shelve as sh

from google import genai
from google.genai import types

from bot.config import GENAI_API
from .config import INSTRUCTIONS

from .chat import GenAIChat


class GoogleGenAI:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=GENAI_API)
        self.__current_model__ = "gemini-2.0-flash-thinking-exp"
        self.k = sh.open("genai.db", flag="c")
        self.default_instruction = INSTRUCTIONS["FRANKLY"]
        self.__normal_chat__ = self.client.aio.chats.create(
            model=self.__current_model__,
            config=self.get_config(),
        )
        self.__managed_chat__ = self.client.aio.chats.create(
            model="gemini-2.0-flash",
            config=self.get_managed_config(),
        )

    def get_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=self.get_instruction(),
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=4096,
            response_mime_type="text/plain",
        )

    def get_managed_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=f"Danh sách các nhân cách: {INSTRUCTIONS}. Sử dụng change_personality('tên nhân cách') để thay đổi nhân cách.",
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=4096,
            response_mime_type="text/plain",
            tools=[
                self.change_personality,
                self.get_instruction,
            ],
        )

    def get_instruction(self) -> str:
        return self.k.get("system_instruction", default=self.default_instruction)

    def set_instruction(self, text: str | None = None):
        if text:
            self.k["system_instruction"] = text
        else:
            del self.k["system_instruction"]

    def change_personality(self, personality: str):
        if personality not in INSTRUCTIONS.keys():
            return "Invalid Personality"
        self.default_instruction = INSTRUCTIONS[personality]
        return "Personality Changed"

    def current_model(self) -> str:
        return self.__normal_chat__._model

    def list_models(self) -> list[str]:
        models = self.client.models.list()
        return [model.name.split("/")[-1] for model in models]

    def switch_model(self, model_name: str) -> None:
        self.__current_model__ = model_name

    def get_chat(self) -> GenAIChat:
        return GenAIChat(self.__normal_chat__)

    def get_managed_chat(self) -> GenAIChat:
        return GenAIChat(self.__managed_chat__)

    def reset_chat(self) -> GenAIChat:
        self.__normal_chat__ = self.client.aio.chats.create(
            model=self.__current_model__,
            config=self.get_config(),
        )
        return GenAIChat(self.__normal_chat__)

    def reset_managed_chat(self) -> GenAIChat:
        self.__managed_chat__ = self.client.aio.chats.create(
            model="gemini-2.0-flash",
            config=self.get_managed_config(),
        )
        return GenAIChat(self.__managed_chat__)
