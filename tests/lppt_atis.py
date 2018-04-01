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

from messagemaker.atis import *
import settings

@ddt
class TestLpptAtis(unittest.TestCase):

    def setUp(self):
        self.airport = settings.AIRPORTS['LPPT']
        self.transition = settings.TRANSITION
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
        self.assertEqual(intro(self.letter, metar), expected)

    @data(
        ('03', '[EXP ILS APCH] [RWY IN USE 03]'),
        ('21', '[EXP ILS Z APCH] [RWY IN USE 21]'),
    )
    @unpack
    def test_approach(self, rwy, expected):
        self.assertEqual(approach(rwy, self.airport), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 11/06 Q942', '[TL] 75'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q943', '[TL] 70'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q959', '[TL] 70'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q960', '[TL] 65'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q976', '[TL] 65'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q978', '[TL] 60'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q994', '[TL] 60'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q996', '[TL] 55'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q1013', '[TL] 55'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q1014', '[TL] 50'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q1031', '[TL] 50'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q1032', '[TL] 45'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q1050', '[TL] 45'),
        ('METAR LPPT 191800Z 35015KT 11/06 Q1051', '[TL] 40'),
    )
    @unpack
    def test_transitionlevel(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(
            transition_level(self.airport, self.transition, metar),
            expected)

    @data(
        ('03', '[AFTER LANDING VACATE VIA HN]'),
        ('21', '[AFTER LANDING VACATE VIA HS] [MEDIUM AND LIGHT AIRCRAFT EXPEC\
T POSITION U FOR DEPARTURE, IF UNABLE ADVISE BEFORE TAXI]'),
        ('35', '')
    )
    @unpack
    def test_arrdepinfo(self, rwy, expected):
        self.assertEqual(
            arrdep_info(self.airport, rwy),
            expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT]'),
        ('METAR LPPT 191800Z 35015KT 350V010 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT] [VRB BTN] 350 [AND] 010 [DEG]'),
        ('METAR LPPT 191800Z 35015G20KT 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT] [MAX] 20 [KT]'),
        ('METAR LPPT 191800Z 35015G20KT 350V010 9999 11/06 Q1016',
        '[WND] 350 [DEG] 15 [KT] [MAX] 20 [KT] [VRB BTN] 350 [AND] 010 [DEG]'),
        ('METAR LPPT 191800Z 00000KT 9999 11/06 Q1016',
        '[WND] [CALM]'),
        ('METAR LPPT 191800Z VRB04KT 9999 11/06 Q1016',
        '[WND] [VRB] 4 [KT]'),
        ('METAR LPPT 191800Z VRB04G10KT 9999 11/06 Q1016',
        '[WND] [VRB] 4 [KT] [MAX] 10 [KT]')
    )
    @unpack
    def test_wind(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(wind(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 11/06 Q1016',
        ''),
        ('METAR LPPT 191800Z 35015KT FEW003 11/06 Q1016',
        '[CLD] [FEW] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT SCT003 11/06 Q1016',
        '[CLD] [SCT] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT BKN003 11/06 Q1016',
        '[CLD] [BKN] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT OVC003 11/06 Q1016',
        '[CLD] [OVC] {300} [FT]'),
        ('METAR LPPT 191800Z 35015KT FEW030 11/06 Q1016',
        '[CLD] [FEW] {3000} [FT]'),
        ('METAR LPPT 191800Z 35015KT FEW100 11/06 Q1016',
        '[CLD] [FEW] {10000} [FT]')
    )
    @unpack
    def test_sky(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(sky(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT FEW000 11/06 Q1016',
        '[CLD] [FEW] {000} [FT]')
    )
    @unpack
    @unittest.expectedFailure
    def test_sky_gndlevel(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(sky(metar), expected, 'see: issue#15')

    @data(
        ('METAR LPPT 191800Z 35015KT FEW040TCU 11/06 Q1016',
        '[CLD] [FEW] [TCU] {4000} [FT]'),
        ('METAR LPPT 191800Z 35015KT FEW020CB 11/06 Q1016',
        '[CLD] [FEW] [CB] {2000} [FT]')
    )
    @unpack
    def test_sky_tcucb(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(sky(metar), expected, 'see: issue#14')

    @data(
        ('METAR LPPT 191800Z 35015KT 10/05 Q1016', '[TEMP] 10'),
        ('METAR LPPT 191800Z 35015KT 05/05 Q1016', '[TEMP] 5'),
        ('METAR LPPT 191800Z 35015KT M10/05 Q1016', '[TEMP] -10'),
        ('METAR LPPT 191800Z 35015KT M05/05 Q1016', '[TEMP] -5'),
    )
    @unpack
    def test_temperature(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(temperature(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 10/10 Q1016', '[DP] 10'),
        ('METAR LPPT 191800Z 35015KT 10/05 Q1016', '[DP] 5'),
        ('METAR LPPT 191800Z 35015KT 10/M10 Q1016', '[DP] -10'),
        ('METAR LPPT 191800Z 35015KT 10/M05 Q1016', '[DP] -5'),
    )
    @unpack
    def test_dewpoint(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(dewpoint(metar), expected)

    @data(
        ('METAR LPPT 191800Z 35015KT 10/10 Q1016', '[QNH] 1016'),
        ('METAR LPPT 191800Z 35015KT 10/10 Q996', '[QNH] 996'),
    )
    @unpack
    def test_qnh(self, metar, expected):
        metar = Metar.Metar(metar)
        self.assertEqual(qnh(metar), expected)
