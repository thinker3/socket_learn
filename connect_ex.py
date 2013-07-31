import socket

baidu = ('www.baidu.com', 80)
netease = ('www.163.com', 80)
twitter = ('twitter.com', 80)

def connect_test(host):
    try:
        soc = socket.socket(2)
        soc.settimeout(5)
        err = soc.connect_ex(host)
        print err, type(err)
        soc.close()
    except socket.gaierror:
        print 'cable error'

connect_test(baidu)
connect_test(netease)
connect_test(twitter)
