"""
messagemaker
Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmai.com>

This file is part of messagemaker.

messagemaker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

messagemaker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with messagemaker.  If not, see <http://www.gnu.org/licenses/>.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ddt import ddt, data, unpack

from messagemaker import message


@ddt
class TestMessageMaker(unittest.TestCase):

    @unpack
    @data(
        {
            'format': '${test}',
            'context': {
                'test': 'true'
            },
            'expected': 'true'
        },
        {
            'format': '[${test}]',
            'context': {
                'test': 'false'
            },
            'expected': '[false]'
        },
        {
            'format': '[WND] [TDZ] ${wind_dir} [DEG] ${wind_speed} [KT]',
            'context': {
                'wind_dir': 240,
                'wind_speed': 7
            },
            'expected': '[WND] [TDZ] 240 [DEG] 7 [KT]'
        }
    )
    def test_makeSubstitute_primative_returnsSelf(
        self, format, context, expected):
        result = message.make_substitute(format, context)
        self.assertEqual(result, expected)
