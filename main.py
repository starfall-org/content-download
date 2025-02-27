import os

import uvloop
from dotenv import load_dotenv

from bg_task import scheduled
from client import make_bot, serve
import asyncio

load_dotenv()
uvloop.install()


def install_uvloop_event_loop():
    if "uvloop" == asyncio.get_event_loop_policy().__module__:
        return

    try:
        import uvloop

        uvloop.install()
    except ImportError as e:
        print(f"Failed to install uvloop: {e}")
    policy = asyncio.get_event_loop_policy()
    print(f"Current event loop policy: {policy.__class__.__name__}")


app = make_bot(
    os.environ["BOT_TOKEN"], os.environ["CONTENT_API"], os.environ["DATABASE_URL"]
)

if __name__ == "__main__":
    install_uvloop_event_loop()
    app.run(serve(app, scheduled))
