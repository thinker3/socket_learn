#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket

HOST = 'localhost'
PORT = 6060

try:
    power = sys.argv[1]
    power = int(power)
except:
    power = 10


def sendall(sock, data, flags=0):
    length = len(data)
    while length > 0:
        ret = sock.send(data, flags)
        if ret == 0:
            __import__('ipdb').set_trace()
        data = data[ret:]
        length = len(data)
    else:
        return None


def my_sendall(sock, data, flags=0):
    big = 10 ** 9
    length = len(data)
    while length > 0:
        if length > big:
            ret = sock.send(data[:big], flags)
        else:
            ret = sock.send(data, flags)
        print ret
        data = data[ret:]
        length = len(data)
    else:
        return None


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
length = 10 ** power
print length
data = 'x' * length
# print client.send(data)  # max: 1410065408
# client.sendall(data)  # sendall not sending all!
# sendall(client, data)
my_sendall(client, data)
client.close()
print '*' * 50
