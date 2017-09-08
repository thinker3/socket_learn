#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

host = ''
port = 6300

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
host, port = client.getsockname()
print port
client.send(str(port))
client.close()
