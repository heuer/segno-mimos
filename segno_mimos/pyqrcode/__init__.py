# -*- coding: utf-8 -*-
#
# Copyright (c) 2013, Michael Nooner
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
PyQRCode <https://github.com/mnooner256/pyqrcode> emulation.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import, unicode_literals
import io
import segno
try:
    str = unicode
except NameError:
    pass

# PyQRCodes provides more notations for error levels
# This dict maps the (non-standard) error levels to a standard indicator
_ERROR_LEVEL = {'7%': 'L', .7: 'L', '15%': 'M', .15: 'M', '25%': 'Q',
                .25: 'Q', '30%': 'H', .30: 'H'}


def create(content, error='H', version=None, mode=None, encoding=None):

    def translate_error(pyqrcode_error):
        try:
            if pyqrcode_error.upper() in ('L', 'M', 'Q', 'H'):
                return pyqrcode_error
        except AttributeError:
            pass
        try:
            return _ERROR_LEVEL[pyqrcode_error]
        except KeyError:
            raise ValueError('Unknown error level "{0}"'.format(pyqrcode_error))

    def translate_mode(pyqrcode_mode):
        mode = pyqrcode_mode
        try:
            mode = pyqrcode_mode.lower()
        except AttributeError:
            pass
        return mode if mode != 'binary' else 'byte'

    return PyQRCode(segno.make_qr(content, error=translate_error(error),
                                  version=version,
                                  mode=translate_mode(mode),
                                  encoding=encoding),
                    content, encoding)


class PyQRCode(object):

    def __init__(self, segno_qrcode, content, encoding):
        self.segno_qrcode = segno_qrcode
        if encoding is None:
            encoding = 'iso-8859-1'
            if segno_qrcode.mode == 'kanji':
                encoding = 'shift_jis'
            elif segno_qrcode.mode == 'byte':
                encoding = 'utf-8'
        if segno_qrcode.mode == 'byte':
            if isinstance(content, bytes):
                try:
                    self.data = content.decode('iso-8859-1')
                except (AttributeError, UnicodeError):
                    self.data = content.decode('utf-8')
            else:
                try:
                    self.data = content.encode('iso-8859-1')
                except UnicodeError:
                    self.data = content.encode('utf-8')

        else:
            try:
                # Bytes?
                self.data = content.decode(encoding)
            except (AttributeError, UnicodeEncodeError):
                try:
                    # str / unicode?
                    self.data = content.encode(encoding)
                except AttributeError:
                    self.data = str(content)
        self.encoding = encoding

    @property
    def code(self):
        try:
            return self._code
        except AttributeError:
            self._code = [[b for b in row] for row in self.segno_qrcode.matrix]
        return self._code

    @property
    def mode(self):
        mode = self.segno_qrcode.mode
        return mode if mode != 'byte' else 'binary'

    @property
    def version(self):
        return self.segno_qrcode.version

    @property
    def error(self):
        return self.segno_qrcode.error

    def show(self, wait=1.2, scale=10, module_color=(0, 0, 0, 255),
             background=(255, 255, 255, 255), quiet_zone=4):
        self.segno_qrcode.show(delete_after=wait, scale=scale,
                               border=quiet_zone, color=module_color,
                               background=background)

    def get_png_size(self, scale=1, quiet_zone=4):
        return self.segno_qrcode.symbol_size(scale=int(scale),
                                             border=quiet_zone)[0]

    def png(self, file, scale=1, module_color=(0, 0, 0, 255),
            background=(255, 255, 255, 255), quiet_zone=4):
        self.segno_qrcode.save(file, kind='png', scale=scale,
                               border=quiet_zone, color=module_color,
                               background=background)

    def png_as_base64_str(self, scale=1, module_color=(0, 0, 0, 255),
                          background=(255, 255, 255, 255), quiet_zone=4):
        data_uri = self.segno_qrcode.png_data_uri(scale=scale, border=quiet_zone,
                                                  color=module_color,
                                                  background=background)
        # PyQRCode does not return a URI but the Base64 encoded PNG
        return data_uri[len('data:image/png;base64,'):]

    def xbm(self, scale=1, quiet_zone=4):
        raise NotImplementedError('This method is not supported')

    def svg(self, file, scale=1, module_color='#000', background=None,
            quiet_zone=4, xmldecl=True, svgns=True, title=None,
            svgclass='pyqrcode', lineclass='pyqrline', omithw=False,
            debug=False):
        if debug:
            import warnings
            warnings.warn('debug is not supported')
        self.segno_qrcode.save(file, kind='svg', scale=scale, border=quiet_zone,
                               color=module_color, background=background,
                               xmldecl=xmldecl, svgns=svgns, title=title,
                               svgclass=svgclass, lineclass=lineclass,
                               omitsize=omithw)

    def eps(self, file, scale=1, module_color=(0, 0, 0),
            background=None, quiet_zone=4):
        self.segno_qrcode.save(file, kind='eps', scale=scale, border=quiet_zone,
                               color=module_color, background=background)

    def text(self, quiet_zone=4):
        out = io.StringIO()
        self.segno_qrcode.save(out, kind='txt', border=quiet_zone, color='1',
                               background='0')
        return out.getvalue()

    def terminal(self, module_color='default', background='reverse',
                 quiet_zone=4):
        if module_color != 'default' \
              or background not in ('reverse', 'reversed', 'inverse', 'inverted'):
            raise NotImplementedError('This method does not implement '
                                      'non-default colors.')
        out = io.StringIO()
        self.segno_qrcode.terminal(out, border=quiet_zone)
        return out.getvalue()
