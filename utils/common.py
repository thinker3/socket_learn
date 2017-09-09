#!/usr/bin/env python
# encoding: utf-8

import socket
import struct
import psutil

import logging
logging.basicConfig(format='[%(asctime)s]---%(levelname)s: %(message)s', level=logging.INFO)

import simplecrypt

key = 'put your own key here'
block_size = 10008
encrypted_block_size = block_size + 68
buffer_size = 1024 * 8
file_name_content_separator = '\r\n'
file_content_crypt_block_separator = '__|__'


def encrypt(data):
    return simplecrypt.encrypt(key, data)


def decrypt(data):
    return simplecrypt.decrypt(key, data)


def create_connection(remote_addr, timeout, source_address):
    domain, port = remote_addr
    remote_ip = socket.gethostbyname(domain)
    ip_port = (remote_ip, port)
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # setsockopt before bind
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if timeout:
        conn.settimeout(timeout)
    if source_address:
        # if not setsockopt, socket.error: [Errno 48] Address already in use
        conn.bind(source_address)
    # socket.error: [Errno 48] Address already in use
    # netstat, TIME_WAIT
    conn.connect(ip_port)
    return conn


def get_tcp_info(sock):
    fmt = "B" * 7 + "I" * 21
    # 'module' object has no attribute 'TCP_INFO'
    x = struct.unpack(
        fmt,
        sock.getsockopt(socket.IPPROTO_TCP, socket.TCP_INFO, 92),
    )
    return x


def get_conn_status(fileno):
    proc = psutil.Process()
    connections = proc.connections()
    matches = [x for x in connections if x.fd == fileno]
    if not matches:
        status = None
    else:
        assert len(matches) == 1
        match = matches[0]
        status = match.status
        return status


def get_data(sock, buf_size=4096):
    data = []
    while True:
        try:
            temp = sock.recv(buf_size)
        except (KeyboardInterrupt, socket.error, socket.timeout) as e:
            print type(e), e
            break
        if not temp:
            break
        data.append(temp)
    data = ''.join(data)
    return data
