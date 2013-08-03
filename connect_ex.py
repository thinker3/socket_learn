import socket

baidu = ('www.baidu.com', 80)
netease = ('www.163.com', 80)
twitter = ('twitter.com', 443)
facebook = ('www.facebook.com', 80)
bank = ('ibsbjstar.ccb.com.cn', 443)
def connect_test(addr):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print soc.getsockname()
        soc.bind(('', 8755))
        print soc.getsockname()
        soc.settimeout(5)
        err = soc.connect_ex(addr)
        print soc.getsockname()
        print soc.getpeername() # socket.error: [Errno 107] Transport endpoint is not connected -- for barred sites or frequent access
        soc.close()
        print '*' * 50

connect_test(baidu)
connect_test(netease)
connect_test(bank)
connect_test(twitter)
connect_test(facebook)
