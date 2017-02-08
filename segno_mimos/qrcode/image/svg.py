# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2017 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
SVG factories.

NOTE: These factories do NOT implement any of the BaseImage methods,
they are just "markers".
"""
from __future__ import absolute_import, unicode_literals
from .base import BaseImage


class SvgFragmentImage(BaseImage):
    kind = 'SVG'
    allowed_kinds = ('SVG',)
    background = None
    config = {'xmldecl': False}


class SvgImage(SvgFragmentImage):
    config = {'xmldecl': True}


class SvgFillImage(SvgImage):
    background = 'white'


SvgPathImage = SvgImage
SvgPathFillImage = SvgFillImage
