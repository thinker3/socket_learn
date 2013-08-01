import sys
syspath = sys.path
syspath.append('/'.join(syspath[0].split('/')[:-1]))

from base.retrospect import get_source_code
import SimpleHTTPServer
import BaseHTTPServer
import SocketServer
import socket

def print_write_src(obj, name):
    src = get_source_code(obj)
    print '-' * 100
    print src
    print '-' * 100
    f = open(name + '_src.py', 'w')
    f.write(src)
    f.close()

#print_write_src(BaseHTTPServer, 'BaseHTTPServer')
#print_write_src(SocketServer, 'SocketServer')
#print_write_src(socket.create_connection, 'create_connection')
print_write_src(socket, 'socket')
