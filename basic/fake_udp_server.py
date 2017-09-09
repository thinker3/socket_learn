import socket, sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('Fake reply', ('127.0.0.1', int(sys.argv[1])))
print 'server address', sock.getsockname()
