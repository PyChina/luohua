#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 落花 / 工具 / 随机性
#
# Copyright (C) 2013-2014 JNRain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals, division

import random
import string


def random_string_from_seq(length, seq):
    rng = random.SystemRandom()
    return ''.join(rng.choice(seq) for i in xrange(length))


def random_salt(length):
    return random_string_from_seq(length, string.ascii_letters)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
