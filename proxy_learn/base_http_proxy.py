#!/usr/bin/env python
# encoding: utf-8

import sys
import urllib
import socket
import select
import shutil
import threading
import datetime as dt
import SocketServer
import BaseHTTPServer
import requests


host = ''
port = 8080
server_addr = (host, port)
lock = threading.Lock()


class Proxy(BaseHTTPServer.BaseHTTPRequestHandler):
    no_proxies = {
        'http': None,
    }

    def do_GET(self, *args, **kwargs):
        lock.acquire()
        #print args  # ()
        #print kwargs  # {}
        print '[do_GET]', dt.datetime.now(), self.raw_requestline
        lock.release()
        self.relay_by_requests()

    def relay_by_requests(self):
        r = requests.get(self.path, headers=self.headers, proxies=self.no_proxies)
        #self.send_headers(r.headers)
        self.wfile.write(r.content)

    def send_headers(self, headers):
        # get plain text
        for k, v in headers.iteritems():
            self.send_header(k, v)
        self.end_headers()

    def get_encoding(self, headers=None, content_type=''):
        if isinstance(headers, dict):
            content_type = headers.get('content-type', '') or content_type
        charset = content_type.split('=')[1:]
        if charset:
            return charset[0].strip()
        else:
            return 'utf-8'

    def get_content_type(self, headers=None, content_type=''):
        if isinstance(headers, dict):
            content_type = headers.get('content-type', '') or content_type
        content_type = content_type.split('; ')[:1]
        if content_type:
            return content_type[0].strip()
        else:
            return ''

    def relay_by_urllib(self):
        shutil.copyfileobj(urllib.urlopen(self.path), self.wfile)

    def do_CONNECT(self):
        # 'https://www.v2ex.com/', for test
        lock.acquire()
        print '[do_CONNECT]', dt.datetime.now(), self.raw_requestline
        lock.release()
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if self._connect_to(self.path, soc):
                #self.log_request(200)
                msg = "%s 200 Connection established\r\n" % self.protocol_version
                self.wfile.write(msg)
                self.wfile.write("Proxy-agent: Test 0.1\r\n")
                self.wfile.write("\r\n")
                self._read_write(soc, 300)
        except socket.error:
            pass
        finally:
            print 'over', self.path
            soc.close()
            self.connection.close()

    def _connect_to(self, netloc, soc):
        i = netloc.find(':')
        if i >= 0:
            host_port = netloc[:i], int(netloc[i + 1:])
        else:
            host_port = netloc, 80
        try:
            soc.connect(host_port)
        except socket.error, arg:
            print unicode(arg)
            try:
                msg = arg[1]
            except:
                msg = arg
            self.send_error(404, msg)
            return 0
        return 1

    def _read_write(self, soc, max_idling=20):
        iw = [self.connection, soc]
        ow = []
        count = 0
        while 1:
            count += 1
            (ins, _, exs) = select.select(iw, ow, iw, 3)
            if exs:
                print 'break due to select exceptions'
                break
            if ins:
                for i in ins:
                    if i is soc:
                        out = self.connection
                    else:
                        out = soc
                    try:
                        data = i.recv(8192)
                    except socket.error as e:
                        print unicode(e)
                        print i == self.connection
                        print e.errno == socket.errno.ECONNRESET
                        raise e
                    if data:
                        print len(data), i.getsockname(), i.getpeername()
                        out.send(data)
                        count = 0
            else:
                pass
                #print "\t idle", count
            if count == max_idling:
                print 'break due to max_idling'
                break

    def do_POST(self):
        lock.acquire()
        print '[do_POST]', dt.datetime.now(), self.raw_requestline
        lock.release()
        content_length = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_length)
        try:
            r = requests.post(self.path, data=post_body, headers=self.headers, proxies=self.no_proxies)
            #self.send_headers(r.headers)
            self.wfile.write(r.content)
        except requests.ConnectionError as e:
            print unicode(e)


if sys.platform == 'win32':
    # on Windows
    # AttributeError: 'module' object has no attribute 'fork'
    httpd = SocketServer.ThreadingTCPServer(server_addr, Proxy)
else:
    httpd = SocketServer.ForkingTCPServer(server_addr, Proxy)
httpd.allow_reuse_address = True  # socket.error: [Errno 98] Address already in use
httpd.serve_forever()
