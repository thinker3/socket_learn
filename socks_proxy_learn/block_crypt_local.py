#! /usr/bin/env python
# encoding: utf-8

import socket
import struct
import traceback
import SocketServer
from select import select
import utils


class Socket5Handler(SocketServer.BaseRequestHandler):
    def handle_tcp(self, remote):
        sock = self.request
        sock_list = [sock, remote]
        try:
            while 1:
                read_list, _, _ = select(sock_list, [], [])
                if remote in read_list:
                    data = remote.recv(utils.config.block_size_encrypted)
                    if (sock.send(utils.decrypt(data)) <= 0):
                        break
                if sock in read_list:
                    data = sock.recv(utils.config.block_size)
                    if (remote.send(utils.encrypt(data)) <= utils.config.block_size_delta):
                        break
        finally:
            remote.close()
            sock.close()

    def handle(self):
        try:
            utils.logging.info("Connection from %s" % str(self.client_address))
            # Here we do not need to recv exact bytes,
            # since we do not require clients to use any auth method
            data = self.request.recv(256)
            if not data or ord(data[0]) != 5:
                raise socket.error("Not socks5")
            # Send initial SOCKS5 response
            self.request.sendall('\x05\x00')
            data = self.request.recv(4)
            ver, cmd, rsv, atyp = [ord(x) for x in data]
            if cmd != 1:
                raise socket.error("Bad cmd value: %d" % cmd)
            if atyp != 3:
                raise socket.error("Bad atyp value: %d" % atyp)
            addr_len = ord(self.request.recv(1))
            addr = self.request.recv(addr_len)
            addr_port = self.request.recv(2)

            # Reply to client to estanblish the socks v5 connection
            reply = "\x05\x00\x00\x01"
            reply += socket.inet_aton('0.0.0.0')
            reply += struct.pack("!H", 0)
            self.request.sendall(reply)

            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect(utils.config.connecting_address)
            utils.logging.info("Connect to %s" % addr)
            addr = utils.encrypt(addr)
            dest_address = "%s%s%s" % (chr(len(addr)), addr, addr_port)
            remote.sendall(dest_address)
            self.handle_tcp(remote)
        except socket.error, e:
            traceback.print_stack()
            utils.logging.warn(e)
        finally:
            self.request.close()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    server = ThreadedTCPServer(utils.config.local_binding_address, Socket5Handler)
    utils.logging.info('Server running at %s ...' % str(utils.config.local_binding_address))
    server.serve_forever()
