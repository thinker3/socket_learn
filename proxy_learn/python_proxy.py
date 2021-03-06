#coding=utf8

import time
import socket
import thread
import select
import threading

__version__ = '0.1.0 Draft 1'
VERSION = 'Python Proxy/'+__version__
BUFLEN = 8192
TIMEOUT = 5
HOST = 'localhost'
PORT = 8080
lock = threading.Lock()


class ConnectionHandler(object):
    def __init__(self, connection, address):
        self.client = connection
        self.client_buffer = ''
        self.timeout = TIMEOUT
        # POST http://www.voanews.com/ HTTP/1.1
        # CONNECT twitter.com:443 HTTP/1.1
        self.method, self.path, self.protocol = self.get_base_header()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE'):
            self.method_others()
        self.client.close()
        if self.target:
            self.target.close()
        show('closed')

    def get_base_header(self):
        while 1:
            time.sleep(0.5)
            self.client_buffer += self.client.recv(BUFLEN)
            end = self.client_buffer.find('\n')
            if end!=-1:
                break
        show(self.client_buffer)
        data = (self.client_buffer[:end+1]).split() # not .split(' ')
        self.client_buffer = self.client_buffer[end+1:]
        return data

    def method_CONNECT(self):
        self._connect_target(self.path) # self.path for instance, twitter.com:443
        self.client.sendall(
                'HTTP/1.1 200 Connection established\r\nProxy-agent: %s\r\n\r\n' % VERSION
                )
        self.client_buffer = ''
        self._read_write()

    def method_others(self):
        #self.path = self.path[7:]
        # http://www.voanews.com/
        self.path = self.path.split('://')[1]
        i = self.path.find('/')
        if i != -1:
            host = self.path[:i]
            path = self.path[i:]
        else:
            host = self.path
            path = '/'
        self._connect_target(host)
        request = '%s %s %s\r\n' % (self.method, path, self.protocol) + self.client_buffer
        show('[%s]' % request)
        self.target.sendall(request)
        self.client_buffer = ''
        self.my_read_write()

    def _connect_target(self, host):
        i = host.find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80
        (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0] # time consuming
        self.target = socket.socket(soc_family, socket.SOCK_STREAM)
        self.target.connect(address)

    def get_data(self, sock):
        data = ''
        try:
            while 1:
                temp = sock.recv(BUFLEN)
                if not temp:
                    break
                data += temp
        except Exception as e:
            print e
        finally:
            return data

    def my_read_write(self):
        data = self.get_data(self.target)
        self.client.sendall(data)

    def _read_write(self):
        time_out_max = self.timeout/3
        socs = [self.client, self.target]
        count = 0
        while 1:
            count += 1
            (recv, _, error) = select.select(socs, [], socs, 3)
            if error:
                break
            if recv:
                for in_ in recv:
                    data = in_.recv(BUFLEN)
                    if in_ is self.client:
                        out = self.target
                    else:
                        out = self.client
                    if data:
                        out.sendall(data)
                        count = 0
            if count == time_out_max:
                break


def show(msg):
    lock.acquire()
    print "%s\r\n" % msg
    lock.release()


def start_server():
    '''
    socket.accept()

    Accept a connection. The socket must be bound to an address and listening for connections. 
    The return value is a pair (conn, address) where conn is a new socket object usable to send and receive data on the connection, 
    and address is the address bound to the socket on the other end of the connection.


    thread.start_new_thread(function, args[, kwargs])

    Start a new thread and return its identifier. 
    The thread executes the function function with the argument list args (which must be a tuple). 
    The optional kwargs argument specifies a dictionary of keyword arguments. 
    When the function returns, the thread silently exits. 
    When the function terminates with an unhandled exception, 
    a stack trace is printed and then the thread exits (but other threads continue to run).
    '''
    soc_type = socket.AF_INET
    soc = socket.socket(soc_type, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind((HOST, PORT))
    soc.listen(0)
    while 1:
        thread.start_new_thread(ConnectionHandler, soc.accept())


if __name__ == '__main__':
    start_server()
