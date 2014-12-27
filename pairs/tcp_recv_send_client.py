#!/usr/bin/env python
# encoding: utf-8

import time
import socket

host = 'localhost'
port = 1060
server_address = (host, port)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    #print s.sendall('hello\r\n')  # None
    #s.send('')  # send() takes at least 1 argument
    #s.sendall('')  # sendall() takes at least 1 argument
    print s.send('hello\r\n')  # 7
    print s.send('')  # 0, but not works
    s.shutdown(socket.SHUT_WR)
    while 1:
        c = s.recv(1)
        print '[%s]' % c.encode('hex')
        time.sleep(0.5)
        if not c:
            break
        '''
        '''
    s.close()
    print '*' * 50

main()
