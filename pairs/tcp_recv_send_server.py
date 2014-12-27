#!/usr/bin/env python
# encoding: utf-8

import socket
import utils

host = ''
port = 1060
server_address = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(server_address)
s.listen(1)

while True:
    sc, _ = s.accept()
    while 1:
        c = sc.recv(1)
        print '[%s]' % c.encode('hex')
        if not c:
            break
    print sc.send('world\r\n')  # 7
    print sc.send('')  # 0, but not works
    sc.close()
    print '*' * 50
