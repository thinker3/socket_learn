#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from utils.common import get_conn_status

HOST = ''
PORT = 6060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_fileno = server.fileno()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
print get_conn_status(server_fileno)  # CLOSE
server.listen(1)
print get_conn_status(server_fileno)  # LISTEN

while True:
    print 'Listening at', server.getsockname()
    try:
        sc, client_addr = server.accept()
    except KeyboardInterrupt:
        server.close()
        break
    client_fileno = sc.fileno()
    print 'We have accepted a connection from', client_addr
    print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
    message = sc.recv(16)
    print 'The incoming message says', repr(message)
    sc.send('Hello')
    sc.sendall('Farewell, client')
    print get_conn_status(client_fileno)
    sc.close()
    print '*' * 50
