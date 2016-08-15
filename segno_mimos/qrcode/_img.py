# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
These classes actually serialize the QR Codes.

They have similar properties as qrcode.image.base.BaseImage but do not
provide the same API (aside from ``save``).

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals, division


class _BaseImage(object):

    kind = None

    def __init__(self, segno_qrcode, box_size, border):
        self._qrcode = segno_qrcode
        self.box_size = box_size  # scale
        self.border = border
        self.width = len(segno_qrcode.matrix)

    def save(self, stream, format=None, **kw):
        raise NotImplementedError()


class DefaultImage(_BaseImage):
    """\
    This class is similar to qrcode.image.pil.PilImage and is able to
    save a QR Code in PNG and EPS format.
    """
    allowed_kinds = ('PNG', 'EPS', 'PDF')

    def __init__(self, qrcode, box_size, border, kind=None):
        super(DefaultImage, self).__init__(qrcode, box_size, border)
        self.kind = kind

    def save(self, stream, format=None, kind=None, **kw):
        fmt = format
        if fmt is None:
            fmt = kind or self.kind
        background_was_set = 'back_color' in kw
        config = dict(scale=self.box_size, border=self.border,
                      color=kw.pop('fill_color', '#000'),
                      background=kw.pop('back_color', '#fff'))
        if config['background'] == 'transparent':
            config['background'] = None
        config.update(kw)
        if fmt in (None, 'PNG', 'png'):
            self._qrcode.png(stream, **config)
            return
        elif fmt in ('EPS', 'eps'):
            # Remove background color if not set explictly
            if not background_was_set:
                config['background'] = None
            self._qrcode.eps(stream, **config)
            return
        elif fmt in ('PDF', 'pdf'):
            # Remove background color if not set explictly
            if not background_was_set:
                config['background'] = None
            self._qrcode.pdf(stream, **config)
            return
        raise ValueError('Unsupported format "{}"'.format(format))


class SVGImage(_BaseImage):
    """\
    This class provides the functionality of the qrcode.image.svg classes.
    Note: The QR Code is always saved as path and never as composition of rects.
    """
    kind = 'SVG'

    def __init__(self, qrcode, box_size, border, config):
        super(SVGImage, self).__init__(qrcode, box_size, border)
        self.config = config

    def save(self, stream, kind=None, **kw):
        if kind not in (None, 'SVG', 'svg'):
            raise ValueError('Unknown kind "{}"'.format(kind))
        # Default config
        conf = dict(scale=self.box_size / 10, unit='mm', svgversion=1.1,
                    border=self.border)
        # Update with factory config
        conf.update(self.config)
        # Let keywords override default config and factory config
        conf.update(kw)
        self._qrcode.svg(stream, **conf)
