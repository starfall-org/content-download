import os
import shelve
import requests


secret_url = os.environ["SECRET"]
shelf = shelve.open("config")


def init():
    req = requests.get(secret_url, timeout=10)
    data = req.json()
    shelf["config_data"] = data


def get_keys():
    data = shelf.get("config_data")
    dapi = data["api"]["dapi"]

    class Keys:
        bot_token = data["access"]["telegram"]["cd"]
        db_url = data["db"]["postgres"][0]
        youtube_api = dapi["yt"]
        music_api = dapi["ytm"]
        facebook_api = dapi["fb"]
        instagram_api = dapi["ig"]
        douyin_api = dapi["td"]

    return Keys


keys = get_keys()
