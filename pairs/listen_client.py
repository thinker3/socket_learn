#!/usr/bin/env python
# encoding: utf-8

import socket
import threading

requests = 10
requests = 20  # 9 connections refused

buf_size = 1
host = 'localhost'
port = 8800
server_addr = (host, port)
lock = threading.Lock()


def get_msg(soc, buf_size):
    msg = ''
    while True:
        temp = soc.recv(buf_size)
        if not temp:
            break
        msg += temp
    return msg


def client(i):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_addr)
        s.sendall('Hi there, server, it is client %d' % i)
        reply = get_msg(s, buf_size)
        print len(reply), i
        s.close()
    except Exception as e:
        lock.acquire()
        print unicode(e)
        print i, 'refused'
        lock.release()


for i in range(requests):
    t = threading.Thread(target=client, args=(i,))
    t.start()
