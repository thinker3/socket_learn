import socket

news = ('news.163.com', 80)

def fetch(addr):
    try:
        sock = socket.create_connection(addr)
        sock.sendall('GET / HTTP/1.1\r\n\r\n')
        data = sock.recv(1024)
        print data
    finally:
        try:
            sock.close()
        except:
            pass

fetch(news)
