#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
from utils.common import get_data

host = ''
port = 6300

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(5)
server.settimeout(1)

clients = set()
data_dict = {}

while True:
    client = None
    try:
        client, _ = server.accept()
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        break
    if client:
        # ESTABLISHED
        # non-blocking?
        # socket.error: [Errno 35] Resource temporarily unavailable
        clients.add(client)
    try:
        readable, writable, exceptional = select.select(
            clients,
            clients,
            clients,
            1
        )
    except KeyboardInterrupt:
        break
    if readable:
        for client in readable:
            data = get_data(client, buf_size=1)
            if data:
                data_dict.setdefault(client, []).append(data)
            else:
                client.close()
                clients.remove(client)

for client in clients:
    client.close()
server.close()
for k, v in data_dict.iteritems():
    print k, ''.join(v)
