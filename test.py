from bot.services.google_genai.core import GoogleGenAI

gg = GoogleGenAI()
for model in gg.models:
    print(model.name)