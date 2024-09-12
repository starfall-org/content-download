import os
import requests
from pydantic import BaseModel

secret_url = os.environ["SECRET"]


class Keys(BaseModel):
    bot_token: str
    db_url: str
    yt_api: str
    ytm_api: str
    fb_api: str
    ig_api: str
    td_api: str


def get_keys():
    req = requests.get(secret_url, timeout=10)
    data = req.json()
    dapi = data["api"]["dapi"]
    return Keys(
        bot_token=data["access"]["telegram"]["cd"],
        db_url=data["db"]["postgres"][0],
        yt_api=dapi["yt"],
        ytm_api=dapi["ytm"],
        fb_api=dapi["fb"],
        ig_api=dapi["ig"],
        td_api=dapi["td"],
    )


keys = get_keys()
