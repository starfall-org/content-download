import sys
from gunicorn.app.wsgiapp import run
from application.contentdownload import runserver
from threading import Threads
def run_web():
  sys.argv = "gunicorn --timeout 1200 --bind 0.0.0.0:3000 application.flask:app".split()
  sys.exit(run())
Thread(target=run_web).start()
runserver()