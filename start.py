import sys, os
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    os.system("python3 main.py runserver &")
    sys.argv = "gunicorn --timeout 1200 --bind 0.0.0.0:3000 application.flask:app".split()
    sys.exit(run())