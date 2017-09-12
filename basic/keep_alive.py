#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from utils import common
from utils.decorators import separate

website = ('www.yinwang.org', 80)


@separate()
def test_close(addr, message, timeout):
    try:
        sock = socket.create_connection(addr, timeout)
    except (ValueError, socket.error) as e:
        print type(e), e
        return
    message = message % addr[0]
    sock.send(message)
    data = common.get_data(sock, buf_size=128)
    print len(data)
    sock.close()


message = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: Close\r\n\r\n"
test_close(website, message, timeout=None)
test_close(website, message, timeout=-1)  # ValueError: Timeout value out of range
test_close(website, message, timeout=0)  # socket.error: [Errno 65] No route to host


def test_keep_alive_and_timeout(addr, message, timeout):
    sock = socket.create_connection(addr, timeout)
    message = message % addr[0]
    sock.send(message)
    data = common.get_data(sock, buf_size=128)
    print len(data)
    sock.close()
    print '*' * 50


def test_keep_alive_and_many_requests(addr, message, timeout):
    sock = socket.create_connection(addr, timeout)
    message = message % addr[0]
    sock.send(message)
    data = common.get_data(sock, buf_size=128)
    print len(data)
    sock.send(message * 2)
    data = common.get_data(sock, buf_size=128)
    print len(data)
    sock.close()
    print '*' * 50


message = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nConnection: keep-alive\r\n\r\n"
test_keep_alive_and_timeout(website, message, timeout=1)
test_keep_alive_and_many_requests(website, message, timeout=None)
