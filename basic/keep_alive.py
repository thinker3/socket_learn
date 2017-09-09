#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from utils.common import get_data

website = ('www.yinwang.org', 80)


def test(addr, message, timeout):
    sock = None
    try:
        sock = socket.create_connection(addr, timeout)
        message = message % addr[0]
        sock.send(message)
        data = get_data(sock, buf_size=128)
        print len(data)
    finally:
        if sock:
            try:
                sock.close()
            except:
                pass
    print '*' * 50


message = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: Close\r\n\r\n"
test(website, message, timeout=None)

message = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: keep-alive\r\n\r\n"
# test(website, message, timeout=-1)  # ValueError: Timeout value out of range
# test(website, message, timeout=0)  # socket.error: [Errno 65] No route to host
test(website, message, timeout=5)
test(website, message, timeout=None)
