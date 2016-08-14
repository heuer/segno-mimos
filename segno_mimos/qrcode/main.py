# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, Lincoln Loop
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
from __future__ import absolute_import, unicode_literals, print_function
import warnings
import segno
from . import constants, exceptions, util, img
from segno.writers import check_valid_scale, check_valid_border
from segno_mimos.qrcode.image.base import BaseImage
try:
    from qrcode.image.base import BaseImage as qrcodeBaseImage
except ImportError:
    qrcodeBaseImage = BaseImage


def make(data=None, **kw):
    qr = QRCode(**kw)
    qr.add_data(data)
    return qr.make_image()


def _check_valid_factory(img_factory):
    if img_factory is not None:
        assert issubclass(img_factory, (BaseImage, qrcodeBaseImage))


class QRCode:

    def __init__(self, version=None, error_correction=constants.ERROR_CORRECT_M,
                 box_size=10, border=4, image_factory=None):
        check_valid_scale(box_size)
        self.version = version and int(version)
        self.error_correction = int(error_correction)
        self.box_size = int(box_size)
        self.border = int(border)
        self.image_factory = image_factory
        _check_valid_factory(image_factory)
        self.clear()

    def clear(self):
        self.modules = None
        self.modules_count = 0
        self.data_cache = None
        self.data_list = []
        self.segno_qrcode = None

    def add_data(self, data, optimize=20):
        if isinstance(data, util.QRData):
            self.data_list.append(data)
        else:
            if optimize:
                chunks = tuple(util.optimal_data_chunks(data))
                self.data_list.extend(chunks)
            else:
                self.data_list.append(util.QRData(data))
        self.data_cache = None

    def make(self, fit=True):
        if fit:
            self.version = None
        self.makeImpl(False, None)

    def makeImpl(self, test, mask_pattern):
        if test is True or mask_pattern is not None:
            warnings.warn('Neither "test" nor "mask_pattern" is supported')
        segno_qrcode = segno.make_qr(self.data_list or '', mode=None,
                                     version=self.version,
                                     error=self.error_correction,
                                     eci=False)
        self.data_cache = True
        self.segno_qrcode = segno_qrcode
        self.modules_count = len(segno_qrcode.matrix)
        self.modules = [[bool(b) for b in row] for row in segno_qrcode.matrix]
        self.version = segno_qrcode.version

    def print_tty(self, out=None):
        if self.data_cache is None:
            self.make()
        print(self.segno_qrcode.terminal(out=out, border=self.border))

    def print_ascii(self, out=None, tty=False, invert=False):
        if self.data_cache is None:
            self.make()
        print(self.segno_qrcode.terminal(out=out, border=self.border))

    def make_image(self, image_factory=None, **kw):
        check_valid_scale(self.box_size)
        check_valid_border(self.border)
        if self.data_cache is None:
            self.make()
        image_factory = image_factory or self.image_factory
        _check_valid_factory(image_factory)
        if image_factory is None or image_factory.kind in ('PNG', 'EPS'):
            return img.DefaultImage(self.segno_qrcode, self.box_size, self.border, image_factory.kind if image_factory is not None else None)
        elif image_factory.kind == 'SVG':
            config = dict(image_factory.config, background=image_factory.background)
            return img.SVGImage(self.segno_qrcode, self.box_size, self.border, config)
        im = image_factory(self.border, self.modules_count, self.box_size, **kw)
        for r in range(self.modules_count):
            for c in range(self.modules_count):
                if self.modules[r][c]:
                    im.drawrect(r, c)
        return im

    def get_matrix(self):
        if self.data_cache is None:
            self.make()
        if not self.border:
            return self.modules
        width = len(self.modules) + self.border*2
        code = [[False]*width] * self.border
        x_border = [False]*self.border
        for module in self.modules:
            code.append(x_border + module + x_border)
        code += [[False]*width] * self.border
        return code
