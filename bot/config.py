import os
import shelve
import requests


shelf = shelve.open("config")


def init():
    secret_url = os.environ["SECRET"]
    req = requests.get(secret_url, timeout=10)
    data = req.json()
    shelf["config_data"] = data


def get_keys():
    data = shelf["config_data"]
    dapi = data["api"]["content"]

    class Keys:
        bot_token = data["telegram"]["bot"]["content"]
        db_url = data["database"]["postgres"][0]
        youtube_api = dapi["yt"]
        music_api = dapi["ytm"]
        facebook_api = dapi["fb"]
        instagram_api = dapi["ig"]
        douyin_api = dapi["td"]

    return Keys


if not shelf.get("config_data"):
    init()
keys = get_keys()
