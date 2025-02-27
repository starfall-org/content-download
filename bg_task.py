import asyncio

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from hydrogram import Client
from scipy.interpolate import PchipInterpolator

from db.client import Database
from db.models import GroupStats, MemberCount


def plot_time_series(data: MemberCount, group_stats: GroupStats):
    title = f"{group_stats.title} - Members Count"
    save_path = f"tmp/{title}|{group_stats.id}.png"
    data.sort(key=lambda x: x.date)
    dates = [item.date for item in data]
    values = [item.count for item in data]
    dates = pd.to_datetime(dates)
    dates_num = mdates.date2num(dates)
    dates_smooth = np.linspace(dates_num.min(), dates_num.max(), 300)
    pchip = PchipInterpolator(dates_num, values)
    values_smooth = pchip(dates_smooth)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(mdates.num2date(dates_smooth), values_smooth, linestyle="-", color="b")
    ax.scatter(dates, values, color="r", zorder=3)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=30, ha="right")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return save_path


def bg_job(c: Client):
    db = Database()
    group_stats = db.get_group_stats()
    loop = asyncio.get_event_loop()
    for gs in group_stats:
        data = db.get_group_stats(gs.id)
        if data:
            path = plot_time_series(data, gs)
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
