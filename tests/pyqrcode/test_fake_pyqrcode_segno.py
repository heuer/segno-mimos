# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2017 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests if install_as_pyqrcode works
"""
from __future__ import absolute_import, unicode_literals
import segno_mimos
import pytest
import io


def test_install_segno_as_pyqrcode():
    segno_mimos.install_as_pyqrcode()
    import pyqrcode
    qr = pyqrcode.create('Hello')
    out = io.BytesIO()
    qr.png(out)
    out.seek(0)
    assert out.getvalue().startswith(b'\211PNG\r\n\032\n')


if __name__ == '__main__':
    pytest.main([__file__])
