"""
Message Maker

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of messagemaker.

Message Maker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

Message Maker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Message Maker.  If not, see <http://www.gnu.org/licenses/>.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ddt import ddt, data, unpack
from metar import Metar

from messagemaker.message import *
import settings

@ddt
class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.airport = settings.AIRPORTS['LPPT']
        self.transition = settings.TRANSITION
        self.letter = 'A'
        self.rwy = '03'

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 SCT027 11/06 Q1016', '03')
    )
    @unpack
    def test_message_doesnotfail(self, metar, rwy):
        self.assertNotEqual(
            message(
                metar,
                rwy,
                self.letter,
                settings.AIRPORTS,
                settings.TRANSITION),
            '')

    @unittest.expectedFailure
    def test_message_windshear_doesnotfail(self):
        self.assertNotEqual(
            message(
                'METAR LPPT 191800Z 35015KT 11/06 Q1016 WS ALL RWYS',
                self.rwy,
                self.letter),
            '',
            'Python Metar module bug, see issue #13')
