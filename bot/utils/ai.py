from ollama import AsyncClient


async def generate_alert(language: str) -> str:
    instruction = {
        "role": "system",
        "content": f"Translate the user's message into the language with language code is '{language}', if you don't know the language or not sure what is that language code, please translate it into English. No extra text, no punctuation, no quotes, just the translated message.",
    }
    message = {
        "role": "user",
        "content": "Hello! I have a few words I'd like to say to you. I have lost my old account and no longer have the authority to manage this bot. Therefore, this bot may cease to function in the future. To continue your experience, you should switch to using **Next Download (@nextdownload_bot)**. However, this does not mean I will shut down this bot, you can still continue to use it as usual.",
    }
    response = await AsyncClient(host="http://63.176.1.134:11434/").chat(
        model="gemma3n:latest", messages=[instruction, message]
    )
    return response["message"]["content"]
