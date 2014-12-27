#!/usr/bin/env python
# encoding: utf-8

import os
import socket
import utils

host = ''
port = 1060
server_address = (host, port)
home = os.path.expanduser('~')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(server_address)
s.listen(1)


def plain():
    while True:
        sc, _ = s.accept()
        file_name = ''
        while 1:
            file_name += sc.recv(utils.buffer_size)
            index = file_name.find(utils.file_name_content_separator)
            utils.logging.info(index)
            if index > 0:
                starter = file_name[index + len(utils.file_name_content_separator):]
                file_name = file_name[:index]
                path_to_save = os.path.join(home, file_name)
                break
        with open(path_to_save, 'w') as f:
            f.write(starter)
            while 1:
                c = sc.recv(utils.buffer_size)
                if not c:
                    f.close()
                    break
                else:
                    f.write(c)
        sc.close()
        utils.logging.info('*' * 50)


def crypt():
    while True:
        sc, _ = s.accept()
        file_name = ''
        while 1:
            file_name += sc.recv(utils.buffer_size)
            index = file_name.find(utils.file_content_crypt_block_separator)
            utils.logging.info(index)
            if index > 0:
                content = file_name[index + len(utils.file_content_crypt_block_separator):]
                file_name = file_name[:index]
                file_name = utils.decrypt(file_name)
                path_to_save = os.path.join(home, file_name)
                break
        with open(path_to_save, 'w') as f:
            while 1:
                content += sc.recv(utils.buffer_size)
                if not content:
                    f.close()
                    break
                else:
                    index = content.find(utils.file_content_crypt_block_separator)
                    while index > 0:
                        block = content[:index]
                        block = utils.decrypt(block)
                        f.write(block)
                        content = content[index + len(utils.file_content_crypt_block_separator):]
                        index = content.find(utils.file_content_crypt_block_separator)
        sc.close()
        utils.logging.info('*' * 50)


def crypt():
    while True:
        sc, _ = s.accept()
        file_name = ''
        while 1:
            file_name += sc.recv(utils.buffer_size)
            index = file_name.find(utils.file_name_content_separator)
            utils.logging.info(index)
            if index > 0:
                content = file_name[index + len(utils.file_name_content_separator):]
                file_name = file_name[:index]
                file_name = utils.decrypt(file_name)
                path_to_save = os.path.join(home, file_name)
                break
        with open(path_to_save, 'w') as f:
            while 1:
                received = sc.recv(utils.buffer_size)
                if not received:
                    if content:
                        block = utils.decrypt(content)
                        f.write(block)
                    f.close()
                    break
                else:
                    utils.logging.info(len(received))
                    content += received
                    while len(content) >= utils.encrypted_block_size:
                        block = content[:utils.encrypted_block_size]
                        content = content[utils.encrypted_block_size:]
                        block = utils.decrypt(block)
                        f.write(block)
        sc.close()
        utils.logging.info('*' * 50)

if __name__ == '__main__':
    try:
        crypt()
    except Exception as e:
        utils.logging.exception(e)
