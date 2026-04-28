from ollama import AsyncClient


async def generate_alert(language: str) -> str:
    instruction = {
        "role": "system",
        "content": f"Translate the user's message into the language with language code is '{language}', if you don't know the language or not sure what is that language code, please translate it into English. Just the translated message naturally, don't add any extra information or explanation.",
    }
    message = {
        "role": "user",
        "content": "Hello! I have lost my old account from last year and no longer have the authority to manage this bot. Therefore, this bot may cease to function in the future. To continue your experience, you should switch to using **Next Download (@nextdownload_bot)**. However, this does not mean I will shut down this bot, you can still continue to use it as usual.",
    }
    response = await AsyncClient(host="http://63.176.1.134:11434/").chat(
        model="gemma3n:latest", messages=[instruction, message]
    )
    return response["message"]["content"]
