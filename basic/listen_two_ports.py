#!/usr/bin/env python
# encoding: utf-8

# test
# http://localhost:8888/
# http://localhost:9999/

from threading import Thread
from threading import Lock
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

lock = Lock()


def serve_on_port(port):
    lock.acquire()
    print 'serving on port', port
    lock.release()
    server = HTTPServer(("", port), SimpleHTTPRequestHandler)
    # try except KeyboardInterrupt does not work
    # c-4: ^\Quit (core dumped)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        exit()


Thread(target=serve_on_port, args=[8888]).start()
serve_on_port(9999)
