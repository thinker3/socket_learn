#!/usr/bin/env python
# coding:utf-8

"""
Originated from goagent/local/proxylib.py
A pure python proxy which does not fuck the GFW
Just for beginners like me to learn how proxy works
"""

import sys
import os
import errno
import time
import struct
import collections
import re
import io
import threading
import thread
import socket
import ssl
import logging
import SocketServer
import BaseHTTPServer
import httplib
import urlparse
import OpenSSL


NetWorkIOError = (socket.error, ssl.SSLError, OpenSSL.SSL.Error, OSError)


def is_clienthello(data):
    if len(data) < 20:
        return False
    if data.startswith('\x16\x03'):
        # TLSv12/TLSv11/TLSv1/SSLv3
        length, = struct.unpack('>h', data[3:5])
        return len(data) == 5 + length
    elif data[0] == '\x80' and data[2:4] == '\x01\x03':
        # SSLv23
        return len(data) == 2 + ord(data[1])
    else:
        return False


def forward_socket(local, remote, timeout, bufsize):
    """forward socket"""
    def __io_copy(dest, source, timeout):
        try:
            dest.settimeout(timeout)
            source.settimeout(timeout)
            while 1:
                data = source.recv(bufsize)
                if not data:
                    break
                dest.sendall(data)
        except socket.timeout:
            pass
        except NetWorkIOError as e:
            if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.ENOTCONN, errno.EPIPE):
                raise
            if e.args[0] in (errno.EBADF,):
                return
        finally:
            for sock in (dest, source):
                try:
                    sock.close()
                except StandardError:
                    pass
    thread.start_new_thread(__io_copy, (remote.dup(), local.dup(), timeout))
    __io_copy(local, remote, timeout)


class LocalProxyServer(SocketServer.ThreadingTCPServer):
    """Local Proxy Server"""
    request_queue_size = 256
    allow_reuse_address = True
    daemon_threads = True

    def close_request(self, request):
        try:
            request.close()
        except StandardError:
            pass

    def finish_request(self, request, client_address):
        try:
            self.RequestHandlerClass(request, client_address, self)
        except NetWorkIOError as e:
            if e[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.EPIPE):
                raise

    def handle_error(self, *args):
        """make ThreadingTCPServer happy"""
        exc_info = sys.exc_info()
        error = exc_info and len(exc_info) and exc_info[1]
        if isinstance(error, NetWorkIOError) and len(error.args) > 1 and 'bad write retry' in error.args[1]:
            exc_info = error = None
        else:
            del exc_info, error
            SocketServer.ThreadingTCPServer.handle_error(self, *args)


class BaseHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Base HTTP Request Handler"""
    def gethostbyname2(self, hostname):
        return socket.gethostbyname_ex(hostname)[-1]

    def create_tcp_connection(self, hostname, port, timeout, **kwargs):
        sock = socket.create_connection((hostname, port), timeout)
        data = kwargs.get('client_hello')
        if data:
            sock.send(data)
        return sock

    def create_ssl_connection(self, hostname, port, timeout, **kwargs):
        sock = self.create_tcp_connection(hostname, port, timeout, **kwargs)
        ssl_sock = ssl.wrap_socket(sock)
        return ssl_sock

    def create_http_request(self, method, url, headers, body, timeout, **kwargs):
        scheme, netloc, path, query, _ = urlparse.urlsplit(url)
        if netloc.rfind(':') <= netloc.rfind(']'):
            # no port number
            host = netloc
            port = 443 if scheme == 'https' else 80
        else:
            host, _, port = netloc.rpartition(':')
            port = int(port)
        if query:
            path += '?' + query
        if 'Host' not in headers:
            headers['Host'] = host
        if body and 'Content-Length' not in headers:
            headers['Content-Length'] = str(len(body))
        ConnectionType = httplib.HTTPSConnection if scheme == 'https' else httplib.HTTPConnection
        connection = ConnectionType(netloc, timeout=timeout)
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        return response


class DirectFetchPlugin(object):
    """direct fetch plugin"""
    connect_timeout = 4
    max_retry = 3

    def handle(self, handler, **kwargs):
        if handler.command != 'CONNECT':
            return self.handle_method(handler, kwargs)
        else:
            return self.handle_connect(handler, kwargs)

    def handle_method(self, handler, kwargs):
        method = handler.command
        if handler.path.lower().startswith(('http://', 'https://', 'ftp://')):
            url = handler.path
        else:
            url = 'http://%s%s' % (handler.headers['Host'], handler.path)
        headers = dict((k.title(), v) for k, v in handler.headers.items())
        body = handler.body
        response = None
        try:
            response = handler.create_http_request(method, url, headers, body, timeout=self.connect_timeout, **kwargs)
            logging.info('%s "DIRECT %s %s %s" %s %s', handler.address_string(), handler.command, url, handler.protocol_version, response.status, response.getheader('Content-Length', '-'))
            response_headers = dict((k.title(), v) for k, v in response.getheaders())
            handler.send_response(response.status)
            for key, value in response.getheaders():
                handler.send_header(key, value)
            handler.end_headers()
            if handler.command == 'HEAD' or response.status in (204, 304):
                response.close()
                return
            need_chunked = 'Transfer-Encoding' in response_headers
            while True:
                data = response.read(8192)
                if not data:
                    if need_chunked:
                        handler.wfile.write('0\r\n\r\n')
                    break
                if need_chunked:
                    handler.wfile.write('%x\r\n' % len(data))
                handler.wfile.write(data)
                if need_chunked:
                    handler.wfile.write('\r\n')
                del data
        except (ssl.SSLError, socket.timeout, socket.error):
            if response:
                if response.fp and response.fp._sock:
                    response.fp._sock.close()
                response.close()
        finally:
            if response:
                response.close()

    def handle_connect(self, handler, kwargs):
        """forward socket"""
        host = handler.host
        port = handler.port
        local = handler.connection
        remote = None
        handler.send_response(200)
        handler.end_headers()
        handler.close_connection = 1
        data = local.recv(1024)
        if not data:
            local.close()
            return
        data_is_clienthello = is_clienthello(data)
        if data_is_clienthello:
            kwargs['client_hello'] = data
        for i in xrange(self.max_retry):
            try:
                remote = handler.create_tcp_connection(host, port, self.connect_timeout, **kwargs)
                if not data_is_clienthello and remote and not isinstance(remote, Exception):
                    remote.sendall(data)
                break
            except StandardError as e:
                logging.exception('%s "FORWARD %s %s:%d %s" %r', handler.address_string(), handler.command, host, port, handler.protocol_version, e)
                if hasattr(remote, 'close'):
                    remote.close()
                if i == self.max_retry - 1:
                    raise
        logging.info('%s "FORWARD %s %s:%d %s" - -', handler.address_string(), handler.command, host, port, handler.protocol_version)
        if hasattr(remote, 'fileno'):
            # reset timeout default to avoid long http upload failure, but it will delay timeout retry :(
            remote.settimeout(None)
        data = data_is_clienthello and getattr(remote, 'data', None)
        if data:
            del remote.data
            local.sendall(data)
        forward_socket(local, remote, 60, bufsize=256*1024)


class SimpleProxyHandler(BaseHTTPRequestHandler):
    """Simple Proxy Handler"""

    bufsize = 256*1024
    protocol_version = 'HTTP/1.1'
    ssl_version = ssl.PROTOCOL_SSLv23
    skip_headers = frozenset(['Vary',
                              'Via',
                              'X-Forwarded-For',
                              'Proxy-Authorization',
                              'Proxy-Connection',
                              'Upgrade',
                              'X-Chrome-Variations',
                              'Connection',
                              'Cache-Control'])
    disable_transport_ssl = True
    scheme = 'http'
    first_run_lock = threading.Lock()
    handler_plugin = DirectFetchPlugin()

    def finish(self):
        """make python2 BaseHTTPRequestHandler happy"""
        try:
            BaseHTTPServer.BaseHTTPRequestHandler.finish(self)
        except NetWorkIOError as e:
            if e[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.EPIPE):
                raise

    def address_string(self):
        return '%s:%s' % self.client_address[:2]

    def send_response(self, code, message=None):
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write('%s %d %s\r\n' % (self.protocol_version, code, message))

    def send_header(self, keyword, value):
        """Send a MIME header."""
        base_send_header = BaseHTTPServer.BaseHTTPRequestHandler.send_header
        keyword = keyword.title()
        if keyword == 'Set-Cookie':
            for cookie in re.split(r', (?=[^ =]+(?:=|$))', value):
                base_send_header(self, keyword, cookie)
        elif keyword == 'Content-Disposition' and '"' not in value:
            value = re.sub(r'filename=([^"\']+)', 'filename="\\1"', value)
            base_send_header(self, keyword, value)
        else:
            base_send_header(self, keyword, value)

    def setup(self):
        if isinstance(self.__class__.first_run, collections.Callable):
            try:
                with self.__class__.first_run_lock:
                    if isinstance(self.__class__.first_run, collections.Callable):
                        self.first_run()
                        self.__class__.first_run = None
            except StandardError as e:
                logging.exception('%s.first_run() return %r', self.__class__, e)
        self.__class__.setup = BaseHTTPServer.BaseHTTPRequestHandler.setup
        self.__class__.do_CONNECT = self.__class__.do_METHOD
        self.__class__.do_GET = self.__class__.do_METHOD
        self.__class__.do_PUT = self.__class__.do_METHOD
        self.__class__.do_POST = self.__class__.do_METHOD
        self.__class__.do_HEAD = self.__class__.do_METHOD
        self.__class__.do_DELETE = self.__class__.do_METHOD
        self.__class__.do_OPTIONS = self.__class__.do_METHOD
        self.__class__.do_PATCH = self.__class__.do_METHOD
        self.setup()

    def first_run(self):
        pass

    def parse_header(self):
        if self.command == 'CONNECT':
            netloc = self.path
        elif self.path[0] == '/':
            netloc = self.headers.get('Host', 'localhost')
            self.path = '%s://%s%s' % (self.scheme, netloc, self.path)
        else:
            netloc = urlparse.urlsplit(self.path).netloc
        m = re.match(r'^(.+):(\d+)$', netloc)
        if m:
            self.host = m.group(1).strip('[]')
            self.port = int(m.group(2))
        else:
            self.host = netloc
            self.port = 443 if self.scheme == 'https' else 80

    def do_METHOD(self):
        self.parse_header()
        self.body = self.rfile.read(int(self.headers['Content-Length'])) if 'Content-Length' in self.headers else ''
        return self.handler_plugin.handle(self)


def test():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s %(message)s\r\n', datefmt='[%b %d %H:%M:%S]')
    server = LocalProxyServer(('', 8080), SimpleProxyHandler)
    logging.info('serving at %r', server.server_address)
    server.serve_forever()


if __name__ == '__main__':
    test()
