#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

baidu = 'www.baidu.com'
netease = 'www.163.com'


def addrinfo_of(host, port=80):
    try:
        info = socket.getaddrinfo(host, port)
        for one in info:
            print one
            (family, socktype, proto, canonname, sockaddr) = one
            assert family == socket.AF_INET
            assert (
                socktype == socket.SOCK_STREAM and proto == socket.IPPROTO_TCP
                or  # noqa
                socktype == socket.SOCK_DGRAM and proto == socket.IPPROTO_UDP
            )
            assert canonname == ''
        print
    except Exception as e:
        print type(e), e


def hostlist_of(host, port=80):
    ips = set()
    x = socket.getaddrinfo(host, port)
    for one in x:
        ip = one[-1][0]
        ips.add(ip)
    return list(ips)


addrinfo_of(baidu)
addrinfo_of(netease)

baidu_ips = hostlist_of(baidu)
print baidu_ips
