import os

import psutil

PROCESS = psutil.Process(os.getpid())


def show_usage(tag=""):
    mem = PROCESS.memory_info().rss / 1024 / 1024
    cpu = PROCESS.cpu_percent(interval=None)
    return f"`[{tag}] CPU: {cpu:5.1f}% | RAM: {mem:7.2f} MB"
