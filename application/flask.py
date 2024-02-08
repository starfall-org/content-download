from flask import Flask
from threading import Thread
import subprocess
import time
import sys
import os

class Webapp(Flask):
    def __init__(self):
        super().__init__('webapp')

app = Webapp()

def restart():
    time.sleep(5)
    os.execl(sys.executable, sys.executable, *sys.argv)

@app.route("/update")
def update_system():
    result = subprocess.run(["bash", "update.sh"], stdout=subprocess.PIPE, text=True)
    return f"<pre>{result.stdout}</pre>"

@app.route("/")
def web_app_home():
    return ""
"""
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      background-color: white;
      color: black;
    }
    a {
      color: blue;
    }
    body.dark-mode {
      background-color: black;
      color: white;
    }
    body.dark-mode a {
      color: orange;
    }
    #link {
      color: green;
    }
    body.dark-mode #link {
      color: orange;
    }
  </style>
  <script>
    function toggleDarkMode() {
      const isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.body.classList.toggle('dark-mode', isDarkMode);
    }
    window.addEventListener('load', toggleDarkMode);
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', toggleDarkMode);
  </script>
</head>
<body>
<b>Content</b>
</body>
</html>
"""