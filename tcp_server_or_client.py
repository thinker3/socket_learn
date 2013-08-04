import socket, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = sys.argv.pop() if len(sys.argv) == 3 else '127.0.0.1'
PORT = 1060
if sys.argv[1:] == ['server']:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print 'Listening at', s.getsockname()
        sc, sockname = s.accept()
        print 'We have accepted a connection from', sockname
        print 'Socket connects', sc.getsockname(), 'and', sc.getpeername()
        message = sc.recv(16)
        print 'The incoming message says', repr(message)
        sc.sendall('Farewell, client')
        sc.close()
        print 'Reply sent, socket closed'
elif sys.argv[1:] == ['client']:
    s.connect((HOST, PORT))
    print 'Client has been assigned socket name', s.getsockname()
    s.sendall('Hi there, server')
    reply = s.recv(16)
    print 'The server said', repr(reply)
    s.close()
else:
    print 'error, usage: python tcp_server_or_client.py server|client [host]'
