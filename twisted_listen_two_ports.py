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
