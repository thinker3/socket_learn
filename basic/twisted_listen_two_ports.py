#!/usr/bin/env python
# encoding: utf-8

from twisted.internet import reactor
from twisted.web import resource, server


class MyResource(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return 'gotten'


site = server.Site(MyResource())

reactor.listenTCP(8888, site)
reactor.listenTCP(9999, site)
reactor.run()
