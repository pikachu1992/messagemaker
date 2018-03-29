"""
messagemaker
Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

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
from metar import Metar

from messagemaker.atis import *
import settings

@ddt
class TestLpptAtis(unittest.TestCase):

    def setUp(self):
        self.airport = settings.AIRPORTS['LPPT']
        self.letter = 'A'

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 SCT027 11/06 Q1016',
        '[LPPT ATIS] [A] 1800'),
        ('METAR LPPT 190530Z 22009KT 9999 -RA FEW012 SCT015 BKN033 12/10 Q1014',
        '[LPPT ATIS] [A] 0530')
    )
    @unpack
    def test_intro(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(intro(self.letter, metar, self.airport), expected)
