#!/usr/bin/env python
# encoding: utf-8
# addition_client.py

import socket
from addition_server import get_msg
from addition_server import port
#from addition_server import server_addr

'''
socket.error: [Errno 10049]
You may use HOST = "" when binding sockets
But when connecting, you should use HOST = "localhost"
'''

host = 'localhost'
server_addr = (host, port)

'''
socket.error: [Errno 10061]
server may be shutdown
'''

'''
https://docs.python.org/2/howto/sockets.html

One way to use shutdown effectively is in an HTTP-like exchange.
The client sends a request and then does a shutdown(1).
This tells the server "This client is done sending, but can still receive."
The server can detect "EOF" by a receive of 0 bytes.
It can assume it has the complete request.
'''

'''
socket.shutdown(how)
Shut down one or both halves of the connection.
If how is SHUT_RD, further receives are disallowed.
If how is SHUT_WR, further sends are disallowed.
If how is SHUT_RDWR, further sends and receives are disallowed.
on Mac OS X, shutdown(SHUT_WR) does not allow further reads on the other end of the connection.
'''

'''
socket.error: [Errno 10048]
c:\home\thin\nuts\git\socket_learn\pairs>NETSTAT.EXE -n|grep 8800
  TCP    127.0.0.1:6060         127.0.0.1:8800         TIME_WAIT
'''

buf_size = 1
runnnig = True
while runnnig:
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.error: [Errno 98] Address already in use
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #soc.bind(('', 6060))  # without this, random port will be assigned
    # socket.error: [Errno 10048], so with this is not a good idea
    soc.connect(server_addr)
    msg = raw_input('> ')
    if not msg:
        soc.close()
    else:
        if msg == 'q':
            runnnig = False
        soc.sendall(msg)
        soc.shutdown(socket.SHUT_WR)
        # only buf_size of the message can be received
        #reply = soc.recv(buf_size)
        reply = get_msg(soc, buf_size)
        print reply
        # socket.error: [Errno 57] Socket is not connected, on Mac
        #soc.shutdown(socket.SHUT_RD)
        soc.close()
