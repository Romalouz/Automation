#!  /usr/bin/env python
from flup.server.fcgi import WSGIServer
from media import media

if __name__ == '__main__':
    WSGIServer(media).run()