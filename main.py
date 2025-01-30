import os
from client import make_bot, serve
from dotenv import load_dotenv

load_dotenv()
app = make_bot(
    os.environ["BOT_TOKEN"], os.environ["CONTENT_API"], os.environ["DATABASE_URL"]
)

if __name__ == "__main__":
    app.run(serve(app))
