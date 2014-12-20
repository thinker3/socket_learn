#!/usr/bin/env python
# encoding: utf-8

import socket

'''
socket.listen(backlog)
Listen for connections made to the socket.
The backlog argument specifies the maximum number of queued connections and should be at least 0;
the maximum value is system-dependent (usually 5), the minimum value is forced to 0.
'''

queue, repeat = 0, 10 ** 5  # ok, on Ubuntu

queue, repeat = 0, 10 ** 6  # not
queue, repeat = 1, 10 ** 6  # not
queue, repeat = 2, 10 ** 6  # not
queue, repeat = 3, 10 ** 6  # not
queue, repeat = 4, 10 ** 6  # not, only one
queue, repeat = 5, 10 ** 6  # ok
queue, repeat = 5, 10 ** 6 * 2  # not
queue, repeat = 6, 10 ** 6 * 2  # not, only one
queue, repeat = 7, 10 ** 6 * 2  # ok

buf_size = 1024
host = ''
port = 8800
server_addr = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(server_addr)
s.listen(queue)

while True:
    sc, client_addr = s.accept()
    print client_addr
    message = sc.recv(buf_size)
    print repr(message)
    sc.sendall('Farewell, client; ' * repeat)
    print 'sendall over'
    sc.close()
    print
