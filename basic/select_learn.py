import select, socket, time

baidu = ('www.baidu.com', 80)
twitter = ('twitter.com', 443)
weibo = ('weibo.com', 80)

def show(lis):
    for sock in lis:
        print sock.getsockname(),
    print

def test():
    try:
        baidu_sock = socket.create_connection(baidu, 3)
        weibo_sock = socket.create_connection(weibo, 3)
        twitter_sock = socket.create_connection(twitter, 3)
        message = "GET / HTTP/1.1\r\n\r\n"
        #message = "GET / HTTP/1.0\r\n\r\n"
        baidu_sock.sendall(message)
        twitter_sock.sendall(message)
        time.sleep(1)
        socks = [baidu_sock, weibo_sock, twitter_sock]
        readable, writable, exceptional = select.select(socks, socks, socks, 5)
        show(readable)
        show(writable)
        show(exceptional)
    except socket.timeout:
        print 'time out' 
    except socket.error, e:
        print 'error %s' % e
    finally:
        print
        for sock in socks:
            try:
                sock.close()
            except:
                pass

test()
