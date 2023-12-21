import uvloop

uvloop.install()
if __name__ == '__main__':
  from application.contentdownload import runserver
  import sys
  if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
    runserver()
