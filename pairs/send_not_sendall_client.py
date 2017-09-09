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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
length = 10 ** power
print length
data = 'x' * length
# print client.send(data)  # max: 1410065408
client.sendall(data)  # sendall not sending all!
client.close()
print '*' * 50
