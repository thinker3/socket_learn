#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

MAX = 65535
PORT = 1060
server = ('127.0.0.1', PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Address before sending:', s.getsockname()
s.sendto('This is my message', server)
print 'Address after sending', s.getsockname()
data, address = s.recvfrom(MAX)
if not address == server:
    print 'attacker', address
    exit()
print 'The server', address, 'says', repr(data)
print 'Address after receiving', s.getsockname()
s.sendto('This is my another message', server)
print 'Address after another sending', s.getsockname()
print
