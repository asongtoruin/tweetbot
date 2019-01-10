#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='tweetbot',
    version='0.0.2',
    description='Basic tweetbot nonsense',
    author='Adam Ruszkowski',
    packages=find_packages(),
    install_requires=['twython']
)
