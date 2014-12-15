#!/usr/bin/env python
# encoding: utf-8
# addition_server.py

import socket

buf_size = 4
host = ''
port = 8800
server_addr = (host, port)

'''
TCP/IP is a stream-based protocol, not a message-based protocol.
You need to define your own message-based protocol on top of TCP in order to differentiate message boundaries.
'''


def get_msg(soc, buf_size):
    msg = ''
    while True:
        temp = soc.recv(buf_size)
        if not temp:
            break
        msg += temp
    return msg

if __name__ == '__main__':
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.error: [Errno 98] Address already in use
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(server_addr)
    print soc.getsockname()
    soc.listen(0)

    runnnig = True
    while runnnig:
        # ctrl+break to KeyboardInterrupt
        client_soc, client_addr = soc.accept()
        print client_addr
        # socket.error: [Errno 104] Connection reset by peer
        #message = client_soc.recv(buf_size)
        message = get_msg(client_soc, buf_size)
        if message == 'q':
            runnnig = False
        numbers = message.split(' ')
        numbers = filter(None, numbers)
        try:
            numbers = map(int, numbers)
            s = sum(numbers)
            numbers = map(str, numbers)
            answer = ' + '.join(numbers)
            answer = '%s = %s' % (answer, s)
        except Exception as e:
            print e
            answer = 'error'
        client_soc.sendall(answer)
        client_soc.close()
    soc.close()
