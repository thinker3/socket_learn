import socket

baidu = ('www.baidu.com', 80)
src_ip = ''
port = 9001
src_addr = (src_ip, port)

allowed_src_ips = [
        '',
        '0.0.0.0',
        '127.0.0.0',
        '192.168.0.0',
        '192.168.0.35',
        ]

problematic_src_ips = [
        '127.0.0.1', # socket.error: [Errno 22] Invalid argument
        '192.168.0.34', # socket.error: [Errno 99] Cannot assign requested address
        ]

def test(addr, src_addr):
    try:
        sock = socket.create_connection(addr, 3, src_addr)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # not working, netstat -na |grep 9001
        print sock.getsockname()
        print sock.getpeername()
        print
        sock.sendall('GET / HTTP/1.1\r\n\r\n')
        data = sock.recv(1024)
        print data
    finally:
        try:
            sock.close()
        except:
            pass

test(baidu, src_addr)
#test(baidu, None) # invariant local ip, varying ports, such as ('192.168.0.35', 57365)
