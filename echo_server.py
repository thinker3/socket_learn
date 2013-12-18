import socket

HOST = ''
PORT = 8000 

if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((HOST, PORT))
    soc.listen(1)
    while True:
        client_soc, client_addr = soc.accept()
        print client_addr 
        message = client_soc.recv(16)
        a, b = message.split('+')
        try:
            c = sum([int(a), int(b)])
            c = str(c) * 10**6 # socket.error: [Errno 104] Connection reset by peer (when power >= 6), when the client close quickly
        except Exception as e:
            print e
            c = 'error'
        client_soc.sendall(c)
        client_soc.close()
