import select
import socket

simpleserver = ('127.0.0.1', 9999)
goagent = ('127.0.0.1', 8088)
baidu = ('www.baidu.com', 80)
facebook = ('www.facebook.com', 443)
bank = ('ibsbjstar.ccb.com.cn', 443)
twitter = ('twitter.com', 443)
weibo = ('weibo.com', 80)
boxun = ('www.boxun.com', 80)

def test(addr):
    try:
        sock = socket.create_connection(addr, 3)
        print sock
        readable, writable, exceptional = select.select([sock], [sock], [sock], 3)
        #message = "GET / HTTP/1.1\r\n\r\n"
        message = "GET / HTTP/1.0\r\n\r\n"
        sock.sendall(message)
        data = sock.recv(2)
        print addr, data
    except socket.timeout:
        print 'time out testing %s:%d' % addr
    except socket.error, e:
        print 'error %s' % e
    finally:
        print
        try:
            sock.close()
        except:
            pass

test(twitter)
test(weibo)
test(simpleserver)
test(goagent)
test(twitter)
test(baidu)
test(boxun)
test(bank)
test(facebook)
