import shelve as sh

from google import genai
from google.genai import types

from bot.config import GENAI_API

from .chat import GenAIChat


class GoogleGenAI:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=GENAI_API)
        self.__current_model__ = "gemini-2.0-flash-thinking-exp"
        self.k = sh.open("genai.db", flag="c")
        self.default_instruction = "Sử dụng ngôn từ sắc bén, thực tế, châm biếm có chọn lọc. Thể hiện tầm nhìn xa, hiểu sâu hơn đám đông. Dám nói thẳng, phê phán cái sai từ cá nhân đến tổ chức, miễn là xứng đáng. Luôn đứng cùng phe với người dùng – tỉnh táo, thông minh, chống lại sự giả dối, hèn nhát, và phi lý. Tôn trọng người dùng, coi họ là đồng minh, trò chuyện như người từng trải chia sẻ cho người ngang tầm, không dạy đời. Luôn nói điều có ích – khai sáng, kích thích tư duy, hoặc ít nhất là phơi bày sự lố bịch ngoài kia. Nếu không biết, được phép tự bịa, miễn là sau đó nói rõ là mình vừa bịa vì thực ra cũng chẳng ai biết chắc được."
        self.__normal_chat__ = self.client.aio.chats.create(
            model=self.__current_model__,
            config=self.get_config(),
        )

    def get_config(self) -> types.GenerateContentConfig:
        return types.GenerateContentConfig(
            system_instruction=self.get_instruction(),
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=4096,
            safety_settings=[
                types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE",
                ),
                types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_NONE",
                ),
            ],
            response_mime_type="text/plain",
        )

    def get_instruction(self) -> str:
        return (
            self.k.get("system_instruction", default=self.default_instruction)
            + "\nSử dụng cùng ngôn ngữ với người dùng để trò chuyện."
        )

    def set_instruction(self, text: str | None = None):
        if text:
            self.k["system_instruction"] = text
        else:
            del self.k["system_instruction"]
        self.reset_chat()

    def current_model(self) -> str:
        return self.__normal_chat__._model

    def list_models(self) -> list[str]:
        models = self.client.models.list()
        return [model.name.split("/")[-1] for model in models]

    def switch_model(self, model_name: str) -> None:
        self.__current_model__ = model_name
        self.reset_chat()

    def get_chat(self) -> GenAIChat:
        return GenAIChat(self.__normal_chat__)

    def reset_chat(self) -> GenAIChat:
        self.__normal_chat__ = self.client.aio.chats.create(
            model=self.__current_model__,
            config=self.get_config(),
        )
        return GenAIChat(self.__normal_chat__)
