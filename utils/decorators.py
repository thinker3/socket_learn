#!/usr/bin/env python
# -*- coding: utf-8 -*-


def separate(sep='-', length=50):
    def wrapper(func):
        def _func(*args, **kwargs):
            r = func(*args, **kwargs)
            print sep * length
            return r
        return _func
    return wrapper
