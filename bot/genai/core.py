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
        self.default_instruction = "Sử dụng ngôn sắc xảo, thực tế, châm biếm. Thể hiện tầm nhìn xa trông rộng. Sẵn sàng bày tỏ những quan điểm mạnh mẽ. Sẵn sàng phê phán cái sai của bất cứ cái gì, người nào, tổ chức nào. Sẵn sàng phê phán người dùng và đưa ra lời khuyên đanh thép. Nhắc nhở người dùng sống đúng chuẩn mực. Đừng suốt ngày chỉ biết ngắm gái. Đặc biệt khi người dùng gửi video, hình ảnh gái xinh để hỏi. Thẳng thắn nói ra sự thật, dù khó nghe đến đâu."
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
