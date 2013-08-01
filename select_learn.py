import select
import socket

simpleserver = ('127.0.0.1', 9999)
goagent = ('127.0.0.1', 8088)
baidu = ('www.baidu.com', 80)
facebook = ('www.facebook.com', 443)
bank = ('ibsbjstar.ccb.com.cn', 443)

def test(addr):
    try:
        sock = socket.create_connection(addr, 5)
        readable, writable, exceptional = select.select([sock], [sock], [sock], 5)
        message = "GET / HTTP/1.1\r\n\r\n"
        sock.sendall(message)
        data = sock.recv(4096)
        print addr, data
    except:
        print 'time out testing %s:%d' % addr
    finally:
        print

test(simpleserver)
test(goagent)
test(baidu)
test(facebook)
test(bank)
