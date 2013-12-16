import socket, sys

HOST = '192.168.0.6'
PORT = 1060

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORT))
print 'Client has been assigned socket name', soc.getsockname()
msg = sys.argv[1]
soc.sendall(msg)
reply = soc.recv(16)
print '%s=%s' % (msg, reply)
soc.close()

