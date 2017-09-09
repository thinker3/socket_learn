#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

news = ('news.163.com', 80)
baidu = ('www.baidu.com', 80)
github = ('github.com', 443)
twitter = ('twitter.com', 443)
digitalocean = ('cloud.digitalocean.com', 443)

timeout = 100  # for bad network service
buf_size = 8192
delimiter = '\r\n'
proxy_addr = ('localhost', 8080)
django_learn = ('localhost', 9010)


class Fetcher(object):
    def __init__(self, target_addr):
        self.target_addr = target_addr
        self.host, self.port = target_addr
        self.sock = socket.create_connection(proxy_addr, timeout)

    def reset_socket(self):
        self.sock = socket.create_connection(proxy_addr, timeout)

    def fetch(self):
        request = '''
        GET http://%s/ HTTP/1.1
        Host: %s
        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
        Connection: Close 
        ''' % (self.host, self.host)
        self.init_request(request)
        self.sock.sendall(self.request)
        data = self.get_data()
        print data[-1000:]

    def get_data(self):
        data = ''
        try:
            while 1:
                temp = self.sock.recv(buf_size) # sometimes blocking even no data left, until timeout, strange
                if not temp:
                    break
                data += temp
        except Exception as e:
            print e
        finally:
            return data

    def connect(self):
        request = '''
        CONNECT %s:%s HTTP/1.1
        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0
        Proxy-Connection: keep-alive
        Connection: keep-alive
        Host: %s 
        ''' % (self.host, self.port, self.host)
        self.init_request(request)
        self.sock.sendall(self.request)
        data = self.get_data()
        print data

    def init_request(self, request):
        line = ''
        for one in request.split('\n'):
            one = one.strip()
            if one:
                line += one + delimiter
        line += delimiter
        self.request = line 

    def ajax_fetch(self):
        request_1 = '''GET http://127.0.0.1:9010/learn/get_unicode/ HTTP/1.1\r\nHost: 127.0.0.1:9010\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'''

        request_2 = '''GET http://127.0.0.1:9010/learn/ajax_get_unicode/ HTTP/1.1\r\nHost: 127.0.0.1:9010\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0\r\nAccept: */*\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nX-Requested-With: XMLHttpRequest\r\nReferer: http://127.0.0.1:9010/learn/get_unicode/\r\nConnection: keep-alive\r\n\r\n'''

        self.sock.send(request_1)
        data = self.get_data()
        print data
        self.close() # how to send twice without close and reset?
        self.reset_socket()
        self.sock.send(request_2)
        data = self.get_data()
        print data

    def close(self):
        try:
            if self.sock:
                self.sock.close()
        except:
            pass


def fetch_test(target_addr):
    browser = Fetcher(target_addr)
    browser.fetch()
    browser.close()


def ajax_fetch_test():
    browser = Fetcher(django_learn)
    browser.ajax_fetch()
    browser.close()


def connect_test(target_addr):
    browser = Fetcher(target_addr)
    browser.connect()
    browser.close()


if __name__ == '__main__':
    #fetch_test(baidu)
    ajax_fetch_test()
    #connect_test(digitalocean)
