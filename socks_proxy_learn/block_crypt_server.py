#! /usr/bin/env python
# encoding: utf-8

import socket
import struct
import SocketServer
from select import select
import utils


class LightHandler(SocketServer.BaseRequestHandler):
    def handle_tcp(self, remote):
        sock = self.request
        sock_list = [sock, remote]
        try:
            while 1:
                read_list, _, _ = select(sock_list, [], [])
                if remote in read_list:
                    data = remote.recv(utils.config.block_size)
                    if (sock.send(utils.encrypt(data)) <= utils.config.block_size_delta):
                        break
                if sock in read_list:
                    data = sock.recv(utils.config.block_size_encrypted)
                    if (remote.send(utils.decrypt(data)) <= 0):
                        break
        finally:
            remote.close()
            sock.close()

    def handle(self):
        try:
            data = self.request.recv(1)
            addr = self.request.recv(ord(data[0]))
            addr = utils.decrypt(addr)
            addr_port = struct.unpack("!H", self.request.recv(2))[0]

            utils.logging.info("Connecting to %s:%s" % (addr, addr_port))
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote.connect((addr, addr_port))
            self.handle_tcp(remote)
        except socket.error, e:
            utils.logging.warn(e)
        finally:
            self.request.close()


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    server = ThreadedTCPServer(utils.config.vps_binding_address, LightHandler)
    utils.logging.info('Server running at %s ...' % str(utils.config.vps_binding_address))
    server.serve_forever()
