#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

baidu = ('www.baidu.com', 80)
https_baidu = ('www.baidu.com', 443)
https_twitter = ('twitter.com', 443)


def test_bind(addr):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.settimeout(3)
    print soc.getsockname()
    soc.bind(('', 8755))
    print soc.getsockname()
    try:
        soc.connect(addr)
        print soc.getsockname()
        print soc.getpeername()
    except socket.error as e:
        # socket.error: [Errno 57] Socket is not connected
        print type(e), e
    soc.close()
    print '*' * 50


test_bind(baidu)
test_bind(https_baidu)
test_bind(https_twitter)
