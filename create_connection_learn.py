import socket

baidu = ('www.baidu.com', 80)
zero = ('0.0.0.0', 9001)

def test(addr, src_addr):
    try:
        sock = socket.create_connection(addr, 3, src_addr)
        print sock.getsockname()
        print
        sock.sendall('GET / HTTP/1.1\r\n\r\n')
        data = sock.recv(1024)
        print data
    finally:
        try:
            sock.close()
        except:
            pass

test(baidu, zero)
#test(baidu, None)
