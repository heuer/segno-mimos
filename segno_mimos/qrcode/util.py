# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, Lincoln Loop
# Copyright (c) 2015 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
This modul provides an excerpt of qrcode.util.
"""
import re
from operator import itemgetter
from segno import consts
from segno.encoder import prepare_data

# QR encoding modes.
MODE_NUMBER = consts.MODE_NUMERIC
MODE_ALPHA_NUM = consts.MODE_ALPHANUMERIC
MODE_8BIT_BYTE = consts.MODE_BYTE
MODE_KANJI = consts.MODE_KANJI


def to_bytestring(data):
    """
    Convert data to a (utf-8 encoded) byte-string if it isn't a byte-string
    already.
    """
    if not isinstance(data, bytes):
        try:
            # Try to use the default byte encoding
            encoding = consts.DEFAULT_BYTE_ENCODING
            data = data.encode(encoding)
        except UnicodeError:
            try:
                # Try Kanji / Shift_JIS
                encoding = consts.KANJI_ENCODING
                data = data.encode(encoding)
            except UnicodeError:
                # Use UTF-8
                encoding = 'utf-8'
                data = data.encode(encoding)
    return data


class QRData(tuple):
    """\
    Data held in a QR compatible format.
    """
    def __new__(cls, data, mode=None, encoding=None, check_data=True):
        seg = prepare_data(data, mode, encoding)[0]
        return tuple.__new__(cls, (seg.data, seg.mode, seg.encoding))

    data = property(itemgetter(0))
    mode = property(itemgetter(1))
    encoding = property(itemgetter(2))

    def __len__(self):
        return len(self.data)

    def write(self, buffer):
        pass

    def __unicode__(self):
        return repr(self)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return repr(self.data)


def optimal_data_chunks(data, minimum=4):
    """
    An iterator returning QRData chunks optimized to the data content.

    :param minimum: The minimum number of bytes in a row to split as a chunk.
    """
    data = to_bytestring(data)
    re_repeat = br'' + ('{{{0},}}'.format(minimum).encode('ascii'))
    num_pattern = re.compile(br'\d' + re_repeat)
    num_bits = _optimal_split(data, num_pattern)
    alpha_pattern = re.compile(br'[' + consts.ALPHANUMERIC_CHARS + br']' + re_repeat)
    for is_num, chunk in num_bits:
        if is_num:
            yield QRData(chunk, mode=MODE_NUMBER, check_data=False)
        else:
            for is_alpha, sub_chunk in _optimal_split(chunk, alpha_pattern):
                if is_alpha:
                    mode = MODE_ALPHA_NUM
                else:
                    mode = MODE_8BIT_BYTE
                yield QRData(sub_chunk, mode=mode, check_data=False)


def _optimal_split(data, pattern):
    while data:
        match = re.search(pattern, data)
        if not match:
            break
        start, end = match.start(), match.end()
        if start:
            yield False, data[:start]
        yield True, data[start:end]
        data = data[end:]
    if data:
        yield False, data

