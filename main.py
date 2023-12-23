from application.contentdownload import runserver
import sys

if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
    runserver()
