import os
import psutil
import time

process = psutil.Process(os.getpid())

def show_usage(tag=""):
    mem = process.memory_info().rss / 1024 / 1024
    cpu = process.cpu_percent(interval=None)
    return f"[{tag}] CPU: {cpu:5.1f}% | RAM: {mem:7.2f} MB"
