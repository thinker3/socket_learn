import socket

baidu = ('www.baidu.com', 80)
netease = ('www.163.com', 80)
twitter = ('twitter.com', 443)
facebook = ('www.facebook.com', 80)
bank = ('ibsbjstar.ccb.com.cn', 443)
def connect_test(addr):
    try:
        soc = socket.socket(2)
        soc.settimeout(5)
        err = soc.connect_ex(addr)
        print err, type(err)
        soc.close()
    except socket.gaierror:
        print 'cable error'

connect_test(baidu)
connect_test(facebook)
connect_test(netease)
connect_test(bank)
connect_test(twitter)
