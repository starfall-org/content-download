import google.generativeai as genai
from config import keys

google_api = keys.google_api


class Gemini:
    def __init__(self, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=google_api)

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        self.instruction = (
            "Mẫu thông tin người dùng: (name: tên, username: username, id: user_id, chat: kiểu chat)."
            + "Câu trả lời của bạn không được chứa phần thông tin người dùng đó, vì nó chỉ là để giúp cho bạn biết ai đang trò chuyện với bạn, id khác nhau thì là những người dùng khác nhau."
            + "Hãy trả lời chính xác, sát với thực tế, tránh trả lời qua loa sai sự thật.Một số câu hỏi có thể là câu hỏi tư duy nên hãy suy xét kỹ trước khi trả lời."
        )

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
            system_instruction=self.instruction,
        )
        self.chat = self.model.start_chat(history=[])

    def reset(self):
        self.chat = self.model.start_chat(history=[])

    def models(self):
        return genai.list_models()

    def info(self):
        return self.model.model_name

    def send(self, m, text, user, file_obj=None):
        if m.sender_chat:
            name = user.title
        elif user.last_name:
            name = user.last_name + " " + user.first_name
        else:
            name = user
        user_id = user.id
        username = user.username
        chat_type = m.chat.type
        if username:
            info = f"(name:         {name}, username: {username}, id: {user_id}, chat: {chat_type})"
        else:
            info = f"(name: {name}, id: {user_id}, chat: {chat_type})"

        if not file_obj:
            message = [text + "\n", info]
        else:
            message = [
                text + "\n",
                info + "\n",
                file_obj,
            ]
        response = self.chat.send_message(message)
        return response.text
