#!/usr/bin/env python
# encoding: utf-8

import socket

host = 'localhost'
port = 6060
server_address = (host, port)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)
    client.send('hello\r\n')
    # client.close()  # socket.error: [Errno 9] Bad file descriptor
    client.shutdown(socket.SHUT_WR)
    while 1:
        char = client.recv(1)
        print '[%s]' % char.encode('hex')
        if not char:
            break
    client.close()
    print '*' * 50


main()
