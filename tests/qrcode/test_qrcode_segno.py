# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Some additional tests against qrcode

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import io
import xml.etree.ElementTree as etree
from nose.tools import eq_, ok_
import segno_mimos.qrcode as qrcode
import segno_mimos.qrcode.image.svg


_SVG_NS = 'http://www.w3.org/2000/svg'


def _get_svg_el(root, name):
    return root.find('{%s}%s' % (_SVG_NS, name))


def _get_path(root):
    return _get_svg_el(root, 'path')


def _get_title(root):
    return _get_svg_el(root, 'title')


def _get_desc(root):
    return _get_svg_el(root, 'desc')


def _parse_xml(buff):
    """\
    Parses XML and returns the root element.
    """
    buff.seek(0)
    return etree.parse(buff).getroot()


def test_svgfragment():
    qr = qrcode.QRCode()
    qr.add_data('test')
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    out = io.BytesIO()
    img.save(out)
    ok_(out.getvalue().startswith(b'<?xml'))
    img = qr.make_image(image_factory=qrcode.image.svg.SvgFragmentImage)
    out = io.BytesIO()
    img.save(out)
    ok_(not out.getvalue().startswith(b'<?xml'))
    ok_(out.getvalue().startswith(b'<svg'))


def test_svgfill_image():
    qr = qrcode.QRCode(image_factory=qrcode.image.svg.SvgFillImage)
    qr.add_data('test')
    img = qr.make_image()
    out = io.BytesIO()
    img.save(out)
    root = _parse_xml(out)
    # Background should be the first path in the doc
    path = _get_path(root)
    ok_(path is not None)
    eq_('#fff', path.attrib.get('fill'))


def test_svgfill_image2():
    qr = qrcode.QRCode(image_factory=SVGFillRed)
    qr.add_data('test')
    img = qr.make_image()
    out = io.BytesIO()
    img.save(out)
    root = _parse_xml(out)
    # Background should be the first path in the doc
    path = _get_path(root)
    ok_(path is not None)
    eq_('red', path.attrib.get('fill'))


def test_change_kind():
    qr = qrcode.QRCode()
    qr.add_data('test')
    img = qr.make_image()
    out = io.BytesIO()
    img.save(out)
    png_magic_no = b'\211PNG\r\n\032\n'
    ok_(out.getvalue().startswith(png_magic_no))
    out = io.BytesIO()
    img.save(out, kind='svg')
    ok_(out.getvalue().startswith(b'<?xml'))


def test_change_format():
    qr = qrcode.QRCode()
    qr.add_data('test')
    img = qr.make_image()
    out = io.BytesIO()
    img.save(out)
    png_magic_no = b'\211PNG\r\n\032\n'
    ok_(out.getvalue().startswith(png_magic_no))
    out = io.BytesIO()
    img.save(out, format='svg')
    ok_(out.getvalue().startswith(b'<?xml'))


def test_eps():
    qr = qrcode.QRCode()
    qr.add_data('test')
    img = qr.make_image()
    out = io.BytesIO()
    img.save(out)
    png_magic_no = b'\211PNG\r\n\032\n'
    ok_(out.getvalue().startswith(png_magic_no))
    out = io.StringIO()
    img.save(out, format='eps')
    ok_(out.getvalue().startswith('%!PS-Adobe-3.0 EPSF-3.0'))


class SVGFillRed(qrcode.image.svg.SvgFillImage):
    background = 'red'


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
