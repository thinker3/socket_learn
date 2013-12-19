import socket

baidu = ('www.baidu.com', 80)
bing = ('cn.bing.com', 80)
src_ip = ''
port = 9001
src_addr = (src_ip, port) # source_address for binding
buf_size = 1024
timeout = 3

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

def get_data(sock):
    data = ''
    try:
        while 1:
            temp = sock.recv(buf_size) # if Connection: keep-alive, it blocks until timeout
            if not temp:
                break
            data += temp
    except Exception as e:
        print e
    finally:
        return data

#message = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: keep-alive\r\n\r\n"
message = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: Close\r\n\r\n"
def test(addr, src_addr):
    global message
    try:
        sock = socket.create_connection(addr, timeout, source_address=None) # socket.error: [Errno 98] Address already in use
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # not working, netstat -na |grep 9001
        print sock.getsockname()
        print sock.getpeername()
        print
        message = message % addr[0]
        sock.send(message)
        data = get_data(sock)
        print data[-1000:]
    finally:
        try:
            sock.close()
        except:
            pass

test(bing, src_addr)
#test(baidu, None) # invariant local ip, varying ports, such as ('192.168.0.35', 57365)
