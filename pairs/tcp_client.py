#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from utils.common import get_conn_status

HOST = 'localhost'
PORT = 6060

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print 'Client has been assigned socket name', client.getsockname()
client.sendall('Hi there, server')
print get_conn_status(client)
while True:
    reply = client.recv(16)
    if not reply:
        client.close()
        break
    print 'The server said', repr(reply)
print '*' * 50
