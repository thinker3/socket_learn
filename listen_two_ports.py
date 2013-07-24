from threading import Thread
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

def serve_on_port(port):
    server = HTTPServer(("", port), SimpleHTTPRequestHandler)
# try except KeyboardInterrupt does not work
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        exit()

Thread(target=serve_on_port, args=[9999]).start()
print 8888
serve_on_port(8888)
# with out Thread, the following does not run
#print 9999
#serve_on_port(9999)

