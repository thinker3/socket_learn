import select
import socket

addr = ('127.0.0.1', 9999)
server = socket.create_connection(addr, 5)
inputs = [server]
outpust = []
r, w, e = select.select(inputs, outpust, inputs, 5) 
for one in (r, w, e, outpust):
    print one

