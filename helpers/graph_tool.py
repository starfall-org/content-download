from datetime import timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator

from database.models import GroupStats, MemberCount


def plot_time_series(data: list[MemberCount], group_stats: GroupStats):
    title = f"{group_stats.title} - Members Count"
    save_path = f"tmp/{title}|{group_stats.id}.png"

    if len(data) < 2:
        print("Không đủ dữ liệu để vẽ biểu đồ.")
        return None

    data.sort(key=lambda x: x.date)
    dates = pd.to_datetime([item.date for item in data])
    values = np.array([item.count for item in data])

    time_diffs = np.diff(dates)
    avg_diff = np.median(time_diffs) if len(time_diffs) > 0 else timedelta(days=1)

    if avg_diff < timedelta(minutes=30):
        resample_rule = "T"
    elif avg_diff < timedelta(hours=6):
        resample_rule = "H"
    elif avg_diff < timedelta(days=2):
        resample_rule = "D"
    elif avg_diff < timedelta(weeks=2):
        resample_rule = "W"
    else:
        resample_rule = "M"

    df = pd.DataFrame({"date": dates, "count": values})
    df = df.set_index("date").resample(resample_rule).mean().dropna()

    dates = df.index.to_pydatetime()
    values = df["count"].values

    dates_num = mdates.date2num(dates)
    if len(dates) > 2:
        dates_smooth = np.linspace(
            dates_num.min(), dates_num.max(), min(300, len(dates) * 2)
        )
        pchip = PchipInterpolator(dates_num, values)
        values_smooth = pchip(dates_smooth)
    else:
        dates_smooth, values_smooth = dates, values

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(mdates.num2date(dates_smooth), values_smooth, linestyle="-", color="b")
    ax.scatter(dates, values, color="r", zorder=3)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))

    plt.xticks(rotation=30, ha="right")
    plt.title(f"{group_stats.title} - Members Count ({resample_rule})")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.6)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    return save_path
