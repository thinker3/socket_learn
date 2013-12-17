import socket

local = ('localhost', 8080)
news = ('news.163.com', 80)
twitter = ('twitter.com', 443)
alipay = ('lab.alipay.com', 443)

def fetch(addr):
    try:
        sock = socket.create_connection(addr, 2)
        print sock.getsockname()
        sock.sendall('GET / HTTP/1.1\r\n\r\n')
        data = sock.recv(1024)
        print data
    except Exception as e:
        print e
    finally:
        try:
            sock.close()
        except:
            pass

def connect(addr):
    try:
        sock = socket.create_connection(local, 2)
        request = 'CONNECT %s:%s HTTP/1.1\r\n\r\n' % addr
        sock.sendall(request)
        data = sock.recv(1024)
        print data
    except Exception as e:
        print e
    finally:
        try:
            sock.close()
        except:
            pass
#fetch(news)
#fetch(twitter)
#connect(alipay)
connect(twitter)
