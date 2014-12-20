import socket

HOST = 'localhost'
PORT = 1060

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print 'Client has been assigned socket name', s.getsockname()
s.sendall('Hi there, server')
reply = s.recv(16)
print 'The server said', repr(reply)
s.close()
print
