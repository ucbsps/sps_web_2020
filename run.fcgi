#!/home/p/ph/physics/sps_web_2020/venv/bin/python
import os
import sys

sys.path.insert(0, os.path.expanduser('~/sps_web_2020'))
from flup.server.fcgi import WSGIServer

import wsgi
if __name__ == '__main__':
    WSGIServer(wsgi.application).run()
