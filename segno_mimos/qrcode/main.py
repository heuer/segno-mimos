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
from . import constants, exceptions, util
from segno.writers import check_valid_scale, check_valid_border
from segno_mimos.qrcode.image.base import BaseImage
try:
    from qrcode.image.base import BaseImage as qrcodeBaseImage
except ImportError:
    qrcodeBaseImage = BaseImage

try:  # pragma: no cover
    range = xrange  # Python 2
except NameError:
    pass


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
        if image_factory is None or image_factory.kind in ('PNG', 'EPS', 'PDF', 'SVG'):
            config = dict(scale=self.box_size, border=self.border)
            kind = None
            if image_factory is not None:
                kind = image_factory.kind
                try:
                    config.update(image_factory.config)
                except AttributeError:
                    pass
                try:
                    config['background'] = image_factory.background
                except AttributeError:
                    pass
            return _Image(self.segno_qrcode, config, kind)
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


class _Image(object):
    """\
    This class is almost similar to qrcode.image.pil.PilImage and is able to
    save a QR Code in all output formats which are common by qrcode and Segno.
    """
    kind = None
    allowed_kinds = ('PNG', 'EPS', 'PDF', 'SVG')

    def __init__(self, segno_qrcode, config, kind):
        self._qrcode = segno_qrcode
        self.default_config = config
        self.width = len(segno_qrcode.matrix)
        self.kind = kind

    def save(self, stream, format=None, kind=None, **kw):
        fmt = format
        if fmt is None:
            fmt = kind or self.kind
        if fmt is not None:
            fmt = fmt.lower()
        config = dict(self.default_config)
        background_was_set = 'back_color' in kw or 'background' in kw or 'background' in config
        config['color'] = kw.pop('fill_color', config.get('color', '#000'))
        config['background'] = kw.pop('back_color', kw.pop('background', config.get('background', '#fff')))
        if config['background'] == 'transparent':
            config['background'] = None
        if fmt == 'svg':
            # SVG default config
            svg_config = dict(scale=config.get('scale', 10) / 10, unit='mm', svgversion=1.1)
            config.update(svg_config)
        config.update(kw)
        if fmt in (None, 'png'):
            self._qrcode.save(stream, kind='png', **config)
            return
        if not background_was_set and fmt in ('eps', 'pdf', 'svg'):
            # Remove background color if not set explictly
            config['background'] = None
        if fmt in ('eps', 'pdf', 'svg'):
            self._qrcode.save(stream, kind=fmt, **config)
            return
        raise ValueError('Unsupported format "{}"'.format(fmt))
