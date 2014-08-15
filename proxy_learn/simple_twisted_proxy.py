#!/usr/bin/env python
# encoding: utf-8

import sys
from twisted.web import proxy, http
from twisted.internet import reactor
from twisted.python import log

port = 8080
log.startLogging(sys.stdout)


class ProxyFactory(http.HTTPFactory):
    protocol = proxy.Proxy


reactor.listenTCP(port, ProxyFactory())
reactor.run()
