# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
import sys

__version__ = '0.1.9'


def install_as_qrcode():
    """\
    Installs Segno Mimos as qrcode so that ``import qrcode`` imports
    segno_mimos.qrcode
    """
    from . import qrcode
    sys.modules['qrcode'] = qrcode


def install_as_pyqrcode():
    """\
    Installs Segno Mimos as PyQRCode so that ``import pyqrcode`` imports
    segno_mimos.pyqrcode
    """
    from . import pyqrcode
    sys.modules['pyqrcode'] = pyqrcode
