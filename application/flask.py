from flask import Flask


app = Flask(__name__)


@app.route("/")
def web_app_home():
    return "OK"
