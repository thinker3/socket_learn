#!/usr/bin/env python
# encoding: utf-8

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
