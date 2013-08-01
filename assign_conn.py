import socket
import copy


def func():
    pass

_cc = socket.create_connection
cc = copy.copy(_cc)
socket.create_connection = func
print _cc
print cc
print socket.create_connection
_cc = None
print cc


def method(a=None,b=0,c=1):
    print a, b, c

socket.getaddrinfo = method
socket.getaddrinfo(1,2)

