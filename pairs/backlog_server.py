#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

host = ''
port = 6300

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
# https://docs.python.org/2/library/socket.html#socket.socket.listen
server.listen(1)  # 没有及时接收的缓存队列长度, backlog

clients = set()

while len(clients) < 3:
    client, client_addr = server.accept()
    clients.add(client)
    print clients
for client in clients:
    print client.recv(1024)
__import__('ipdb').set_trace()
server.close()
