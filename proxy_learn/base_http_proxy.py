#!/usr/bin/env python
# encoding: utf-8

import datetime as dt
import urllib
import shutil
import threading
import SocketServer
import BaseHTTPServer

PORT = 8080
lock = threading.Lock()


class Proxy(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        lock.acquire()
        print dt.datetime.now(), self.raw_requestline
        lock.release()
        shutil.copyfileobj(urllib.urlopen(self.path), self.wfile)


#httpd = SocketServer.ForkingTCPServer(('127.0.0.1', PORT), Proxy)
"""
Exception happened during processing of request from ('127.0.0.1', 60329)
Traceback (most recent call last):
  File "c:\python26\lib\SocketServer.py", line 283, in _handle_request_noblock
    self.process_request(request, client_address)
  File "c:\python26\lib\SocketServer.py", line 525, in process_request
    pid = os.fork()
AttributeError: 'module' object has no attribute 'fork'
"""
httpd = SocketServer.ThreadingTCPServer(('127.0.0.1', PORT), Proxy)
httpd.serve_forever()
