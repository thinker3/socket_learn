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

def hostlist_of(host, port=80):
    x = socket.getaddrinfo(host, port)
    for one in x:
        yield one[-1][0]


#addrinfo_of(baidu)
#addrinfo_of(facebook)
#addrinfo_of(netease)
#addrinfo_of(bank)
addrinfo_of(twitter, 443)
twitter_ips = list(set(hostlist_of(twitter, 443)))
baidu_ips = list(set(hostlist_of(baidu)))

print twitter_ips
print baidu_ips
print twitter_ips or baidu_ips
print [''] or baidu_ips
