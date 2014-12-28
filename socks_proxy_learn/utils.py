#!/usr/bin/env python
# encoding: utf-8

import logging
logging.basicConfig(format='[%(asctime)s]---%(levelname)s: %(message)s', level=logging.INFO)

try:
    import your_config as config
except:
    import config
import simplecrypt


def encrypt(data):
    return simplecrypt.encrypt(config.key, data)


def decrypt(data):
    return simplecrypt.decrypt(config.key, data)
