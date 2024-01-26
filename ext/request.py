from requests import Session

session = Session(proxies={"http":"http://127.0.0.1:8090", "https":"http://127.0.0.1:8090"})