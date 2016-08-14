#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Setup script.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
from setuptools import setup
import os
import io
import re


def read(*filenames, **kwargs):
    base_path = os.path.dirname(os.path.realpath(__file__))
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(os.path.join(base_path, filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

version = '0.1.0'# re.search(r'''^__version__ = ["']([^'"]+)['"]''',
                 #   read('segno_mimos/pyqrcode/__init__.py'), flags=re.MULTILINE).group(1)

setup(
    name='segno-mimos',
    version=version,
    url='https://github.com/heuer/segno-mimos/',
    description='Emulating PyQRCode and Python-QR Code API using the Segno (Micro) QR Code generator',
    long_description=read('README.rst', 'CHANGES.rst'),
    license='BSD',
    author='Lars Heuer',
    author_email='heuer[at]semagia.com',
    platforms=['any'],
    install_requires=['segno'],
    include_package_data=True,
    keywords=['QR Code', 'Micro QR Code', 'ISO/IEC 18004',
              'ISO/IEC 18004:2006(E)', 'ISO/IEC 18004:2015(E)'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
