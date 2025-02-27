import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from hydrogram import Client

from db.client import Database
from utils.tools import plot_time_series


def bg_job(c: Client):
    db = Database()
    group_stats = db.get_group_stats()
    loop = asyncio.get_event_loop()
    for gs in group_stats:
        path = plot_time_series(gs.member_count, gs)
        asyncio.run_coroutine_threadsafe(c.send_photo(gs.id, photo=path), loop=loop)


def scheduled(c: Client):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        bg_job,
        "cron",
        args=[c],
        hour=5,
    )
    scheduler.start()
