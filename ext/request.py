import requests
from .var import proxies

def request_get(url):
    try:
        r = requests.get(url)
        if not r.content or not isinstance(r.content, bytes):
            raise
    except:
        r = requests.get(url, proxies=proxies)
    return r.content
    