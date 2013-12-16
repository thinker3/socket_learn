import socket

HOST = ''
PORT = 1060

if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((HOST, PORT))
    soc.listen(1)
    while True:
        sc, sockname = soc.accept()
        message = sc.recv(16)
        a, b = message.split('+')
        try:
            c = sum([int(a), int(b)])
            c = str(c)
        except:
            c = 'error'
        sc.sendall(c)
        sc.close()
