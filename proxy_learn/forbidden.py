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
    host, port = addr
    request = '''
    CONNECT %s:%s HTTP/1.1
    User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
    Proxy-Connection: keep-alive
    Connection: keep-alive
    Host: %s 
    ''' % (host, port, host)
    delimiter = '\r\n'
    def clear_request(request):
        for one in request.split('\n'):
            one = one.strip()
            if one:
                yield one
    request = delimiter.join(clear_request(request))
    request += delimiter * 2
    try:
        sock = socket.create_connection(local, 2)
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
