# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests if install_as_qrcode works

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import segno_mimos
import pytest
import io


def test_svgfragment():
    segno_mimos.install_as_qrcode()
    import qrcode
    import qrcode.image.svg
    qr = qrcode.QRCode(image_factory=qrcode.image.svg.SvgFragmentImage)
    qr.add_data('test')
    img = qr.make_image()
    out = io.BytesIO()
    img.save(out)
    out.seek(0)
    assert out.getvalue().startswith(b'<svg')


if __name__ == '__main__':
    pytest.main([__file__])
