#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

remote = ('', 6300)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(remote)
client.send('')
__import__('ipdb').set_trace()
client.close()
