#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from utils.common import (
    create_connection,
)

zero = ('0.0.0.0', 9001)
empty = ('', 9001)
timeout = 3
allowed_src_ips = [
    '',
    '0.0.0.0',
    '127.0.0.0',
    '192.168.0.0',
    '192.168.0.35',
]

problematic_src_ips = [
    '127.0.0.1',  # socket.error: [Errno 22] Invalid argument
    '192.168.0.34',  # socket.error: [Errno 99] Cannot assign requested address
]


def test(source_address):
    target = ('www.baidu.com', 80)
    target = ('www.v2ex.com', 80)
    sock = None
    try:
        # sock = socket.create_connection(target, timeout, source_address)
        sock = create_connection(target, timeout, source_address)
        print 'source_address: %s' % (source_address, )
        print sock.getsockname()
        print sock.getpeername()
        sock.sendall('GET / HTTP/1.1\r\n\r\n')
        data = sock.recv(1024)
        print 'data length: %s' % len(data)
    except socket.error as e:
        print type(e), e
    finally:
        if sock:
            try:
                sock.close()
            except Exception as e:
                print type(e), e


if __name__ == '__main__':
    test(empty)
    test(zero)
    test(None)
    pass
