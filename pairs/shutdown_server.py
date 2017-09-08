#!/usr/bin/env python
# encoding: utf-8

import socket

host = ''
port = 6060
server_address = (host, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(server_address)
server.listen(1)

while True:
    try:
        conn, _ = server.accept()
    except KeyboardInterrupt:
        server.close()
        break
    while 1:
        char = conn.recv(1)
        print '[%s]' % char.encode('hex')
        if not char:
            break
    conn.send('world\r\n')
    conn.shutdown(socket.SHUT_WR)
    conn.close()
    print '*' * 50
