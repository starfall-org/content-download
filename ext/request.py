import requests

session = requests.Session(proxies={"http":"http://127.0.0.1:8090", "https":"http://127.0.0.1:8090"})

def request_get(url):
    try:
        r = requests.get(url, timeout=5)
        if not r.content or not isinstance(r.content, bytes):
            raise
    except:
        r = session.get(url)
    return r.content
    