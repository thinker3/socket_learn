#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import time
import socket
import utils

host = 'localhost'
port = 1060
server_address = (host, port)


def get_abs_file_path():
    if sys.argv[1:]:
        file_name = sys.argv[1]
    else:
        file_name = sys.argv[0]
    return os.path.abspath(file_name)


def plain():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    s.sendall(os.path.basename(get_abs_file_path()))
    s.send(utils.file_name_content_separator)
    #s.sendall(utils.file_name_content_separator)
    with open(get_abs_file_path(), 'rb') as f:
        while 1:
            if s.send(f.read(utils.block_size)) <= 0:
                break
    s.shutdown(socket.SHUT_WR)
    s.close()
    utils.logging.info('*' * 50)


def crypt():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    basename = os.path.basename(get_abs_file_path())
    basename = utils.encrypt(basename)
    s.send(basename)
    s.send(utils.file_content_crypt_block_separator)
    with open(get_abs_file_path(), 'rb') as f:
        while 1:
            block = f.read(utils.block_size)
            if block:
                block = utils.encrypt(block)
                utils.logging.info(len(block))
                s.send(block)
                s.send(utils.file_content_crypt_block_separator)
            else:
                break
    s.shutdown(socket.SHUT_WR)
    s.close()
    utils.logging.info('*' * 50)


def crypt():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    basename = os.path.basename(get_abs_file_path())
    basename = utils.encrypt(basename)
    s.send(basename)
    s.send(utils.file_name_content_separator)
    with open(get_abs_file_path(), 'rb') as f:
        while 1:
            block = f.read(utils.block_size)
            if block:
                block = utils.encrypt(block)
                utils.logging.info(len(block))
                s.send(block)
            else:
                break
    s.shutdown(socket.SHUT_WR)
    s.close()
    utils.logging.info('*' * 50)

if __name__ == '__main__':
    try:
        crypt()
    except Exception as e:
        utils.logging.exception(e)
