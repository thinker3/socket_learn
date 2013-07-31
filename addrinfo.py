import socket

baidu = 'www.baidu.com'
netease = 'www.163.com'
twitter = 'twitter.com'
facebook = 'www.facebook.com'
bank = 'ibsbjstar.ccb.com.cn'

def addrinfo_of(host, port=80):
    try:
        a = socket.getaddrinfo(host, port)
        print a
        print
    except Exception as e:
        print e

addrinfo_of(baidu)
#addrinfo_of(facebook)
#addrinfo_of(netease)
#addrinfo_of(bank)
addrinfo_of(twitter, 443)
