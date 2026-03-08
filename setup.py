#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Zzz(1309458652@qq.com)
# Description:

from setuptools import setup, find_packages

setup(
    name = 'musicz_pygm',
    version = '0.1.1',
    keywords='musicz_pygm',
    long_description=open('README.md', 'r', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    description = "键盘弹钢琴，keyboard to play piano",
    license = 'Apache License 2.0',
    url = 'https://github.com/buildCodeZ/musicz_pygm',
    author = 'Zzz',
    author_email = '1309458652@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = ['buildz>=0.9.14','pygame>=2.6.0'],
)
