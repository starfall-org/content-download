#!/bin/env python
import uvloop
uvloop.install()

if __name__ == '__main__':
    from application import Content
    Content().run()
