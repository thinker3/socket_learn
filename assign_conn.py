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

