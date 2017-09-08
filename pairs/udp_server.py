#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

MAX = 65535
PORT = 1060

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', PORT))
print 'Listening at', s.getsockname()

while True:
    data, address = s.recvfrom(MAX)
    print 'The client at', address, 'says', repr(data)
    reply = 'Your data was [[%s]], %d bytes' % (data, len(data))
    s.sendto(reply, address)
