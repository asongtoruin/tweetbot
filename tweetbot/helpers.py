#!/usr/bin/env python
# -*- coding: utf-8 -*-


def read_key_from_file(input_file):
    with open(input_file, 'r') as f:
        return f.read()
