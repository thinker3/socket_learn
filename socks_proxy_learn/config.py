#! /usr/bin/env python
# encoding: utf-8

key = 'put you own encrypt/decrypt key here'

block_size = 1008 * 8
block_size_delta = 68
block_size_encrypted = block_size + block_size_delta

vps_ip = '127.0.0.1'
vps_binding_ip = '127.0.0.1'
vps_binding_port = 8388
local_binding_ip = '127.0.0.1'
local_binding_port = 1080

vps_binding_address = (vps_binding_ip, vps_binding_port)
local_binding_address = (local_binding_ip, local_binding_port)
connecting_address = (vps_ip, vps_binding_port)
