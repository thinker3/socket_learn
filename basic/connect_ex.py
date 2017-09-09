#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

baidu = ('www.baidu.com', 80)
https_baidu = ('www.baidu.com', 443)
https_twitter = ('twitter.com', 443)


def test_connect(addr):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(('', 8755))
    soc.settimeout(5)
    try:
        soc.connect(addr)
        print soc.getsockname()
        print soc.getpeername()
    except (socket.error, socket.timeout) as e:
        print type(e), e
    finally:
        soc.close()
    print '*' * 50


def test_connect_ex(addr):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(('', 8755))
    soc.settimeout(5)
    errno = soc.connect_ex(addr)
    print 'errno: %s' % errno
    print soc.getsockname()
    try:
        print soc.getpeername()
    except socket.error as e:
        # socket.error: [Errno 57] Socket is not connected
        assert errno in [35, 48]
        print type(e), e
    soc.close()
    print '*' * 50


test_connect(baidu)
test_connect(https_baidu)
test_connect(https_twitter)

test_connect_ex(baidu)
test_connect_ex(https_baidu)
test_connect_ex(https_twitter)
