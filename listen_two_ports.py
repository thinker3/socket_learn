from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello World!")

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def serve_on_port(port):
    server = ThreadingHTTPServer(("localhost",port), Handler)
    server.serve_forever()

Thread(target=serve_on_port, args=[1111]).start()
serve_on_port(2222)


from twisted.internet import reactor
from twisted.web import resource, server

class MyResource(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        return 'gotten'

site = server.Site(MyResource())

reactor.listenTCP(8000, site)
reactor.listenTCP(8001, site)
reactor.run()
