#!/usr/bin/env python
# encoding: utf-8

import socket


def separate():
    print '-' * 100

separate()
host = 'www.baidu.com'
port = 80
buffersize = 1024
buffersize = 1024 / 2

message = "GET / HTTP/1.1\r\n\r\n"  # HTTP/1.1 302 Moved Temporarily
# long string, long_string, longstr
message = (
    'GET / HTTP/1.1\r\n'
    'Host: www.baidu.com\r\n'
    'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\n'
    'Connection: keep-alive\r\n\r\n'
)
print message
separate()
print message,


separate()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(host)
print ip  # such as 112.80.248.73
#s.connect((ip, port))
s.connect((host, port))  # both are ok
s.sendall(message)
reply = s.recv(buffersize)
print reply
s.close()


separate()
s = socket.create_connection((host, port))
s.sendall(message)
reply = s.recv(buffersize)
print reply
s.close()

separate()
