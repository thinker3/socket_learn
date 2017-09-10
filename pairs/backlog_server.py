#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from utils.common import get_conn_status

host = ''
port = 6300

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
# https://docs.python.org/2/library/socket.html#socket.socket.listen
server.listen(1)  # 没有及时接收的缓存队列长度, backlog
server.settimeout(10)

clients = []
clients = set()

while len(clients) < 3:
    try:
        client, client_addr = server.accept()
    except socket.timeout:
        break
    if isinstance(clients, set):
        clients.add(client)
    else:
        clients.append(client)
    print clients
# __import__('time').sleep(0.5)
for client in clients:
    try:
        print client.recv(1024)
    except socket.error as e:
        # socket.error: [Errno 35] Resource temporarily unavailable
        print type(e), e
        print get_conn_status(client.fileno())
        # can not catch that bad status
        print client.recv(1024)
__import__('ipdb').set_trace()
for client in clients:
    client.close()
server.close()
