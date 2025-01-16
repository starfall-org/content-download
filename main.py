import os
import anyio
from content.client import make_bot
from config import set_envs

set_envs()
app = make_bot(
    os.environ["BOT_TOKEN"], os.environ["CONTENT_API"], os.environ["DATABASE_URL"]
)

if __name__ == "__main__":
    anyio.run(app.online())
