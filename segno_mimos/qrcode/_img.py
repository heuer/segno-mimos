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


class QRCodeImage(object):
    """\
    This class is almost similar to qrcode.image.pil.PilImage and is able to
    save a QR Code in all output formats which are common by qrcode and Segno.
    """
    kind = None
    allowed_kinds = ('PNG', 'EPS', 'PDF', 'SVG')

    def __init__(self, segno_qrcode, box_size, border, config, kind):
        self._qrcode = segno_qrcode
        self.box_size = box_size  # scale
        self.border = border
        self.config = config
        self.width = len(segno_qrcode.matrix)
        self.kind = kind

    def save(self, stream, format=None, kind=None, **kw):
        fmt = format
        if fmt is None:
            fmt = kind or self.kind
        if fmt is not None:
            fmt = fmt.lower()
        background_was_set = 'back_color' in kw
        config = dict(scale=self.box_size, border=self.border,
                      color=kw.pop('fill_color', '#000'),
                      background=kw.pop('back_color', '#fff'))
        if config['background'] == 'transparent':
            config['background'] = None
        config.update(kw)
        if fmt in (None, 'png'):
            self._qrcode.save(stream, kind='png', **config)
            return
        if not background_was_set and fmt in ('eps', 'pdf', 'svg'):
            # Remove background color if not set explictly
            config['background'] = None
        if fmt in ('eps', 'pdf'):
            self._qrcode.save(stream, kind=fmt, **config)
            return
        elif fmt == 'svg':
            # Default qrcode SVG config
            svg_config = dict(scale=self.box_size / 10, unit='mm', svgversion=1.1,
                        border=self.border)
            config.update(svg_config)
            self._qrcode.save(stream, kind='svg', **config)
            return
        raise ValueError('Unsupported format "{}"'.format(format))
