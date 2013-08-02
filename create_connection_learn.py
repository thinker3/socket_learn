import socket

simpleserver = ('127.0.0.1', 9999)
goagent = ('127.0.0.1', 8088)
baidu = ('www.baidu.com', 80)
facebook = ('www.facebook.com', 443)
bank = ('ibsbjstar.ccb.com.cn', 443)
twitter = ('twitter.com', 443)
weibo = ('weibo.com', 80)
boxun = ('www.boxun.com', 80)


zero = ('0.0.0.0', 9001)
local = ('127.0.0.1', 9002)
empty = ('', 9003)

def test(addr, src_addr):
    try:
        sock = socket.create_connection(addr, 3, src_addr)
        print sock
    except:
        print 'test_src_addr', src_addr, 'failed' 
    finally:
        print
        try:
            sock.close()
        except:
            pass

test(simpleserver, local)
test(weibo, zero)
test(baidu, empty)
