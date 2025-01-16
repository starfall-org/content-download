import os
import shelve
import requests


def set_envs():
    shelf = shelve.open("config")
    if not shelf.get("config_data"):
        secret_url = os.environ["SECRET"]
        req = requests.get(secret_url, timeout=10)
        data = req.json()
        shelf["config_data"] = data

    data = shelf["config_data"]
    envs = {
        "BOT_TOKEN": data["telegram"]["bot"]["content"],
        "DATABASE_URL": data["database"]["postgres"][0],
        "GOOGLE_API": data["key"]["google_ai"],
        "CONTENT_API": data["api"]["content"],
    }
    os.environ.update(envs)
