from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def serve_on_port(port):
    server = ThreadingHTTPServer(("", port), SimpleHTTPRequestHandler)
    server.serve_forever()

Thread(target=serve_on_port, args=[9999]).start()
serve_on_port(8888)

