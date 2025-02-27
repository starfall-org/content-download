import uvloop
from gevent import monkey

uvloop.install()
monkey.patch_all()
import os

from dotenv import load_dotenv

from bg_task import scheduled
from client import make_bot, serve

load_dotenv()
app = make_bot(
    os.environ["BOT_TOKEN"], os.environ["CONTENT_API"], os.environ["DATABASE_URL"]
)

if __name__ == "__main__":
    app.run(serve(app, scheduled))
