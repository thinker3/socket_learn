#!/usr/bin/env python
# encoding: utf-8

import sys
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

if sys.argv[1:]:  # slicing can prevent index out of range
    port = int(sys.argv[1])
else:
    port = 9999
server_address = ('127.0.0.1', port)  # Serving HTTP on 127.0.0.1 port 9999 ...
server_address = ('0.0.0.0', port)  # Serving HTTP on 0.0.0.0 port 9999 ...
server_address = ('', port)  # Serving HTTP on 0.0.0.0 port 9999 ...

httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
socketname = httpd.socket.getsockname()
print "Serving HTTP on", socketname[0], "port", socketname[1], "..."
httpd.serve_forever()
