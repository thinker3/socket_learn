#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

HOST = ''
PORT = 6060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(0)


def count(data):
    length = 0
    for one in data:
        length += len(one)
    return length


while True:
    try:
        sc, client_addr = server.accept()
    except KeyboardInterrupt:
        server.close()
        break
    data = []
    while True:
        temp = sc.recv(4096)
        if not temp:
            break
        data.append(temp)
    print count(data)
    sc.close()
    print '*' * 50
