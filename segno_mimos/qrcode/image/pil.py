# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
PNG Image factory

NOTE: This factory does NOT implement any of the BaseImage methods, it's just
a "marker".
"""
from __future__ import absolute_import, unicode_literals
from .base import BaseImage


class PilImage(BaseImage):

    kind = 'PNG'

