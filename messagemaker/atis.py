"""
Message Maker

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmai.com>

This file is part of Message Maker.

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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from string import Template
from metar import Metar
from messagemaker import *
from bisect import bisect_right


def message(metar, deprwy, arrrwy, atiscode):
    metar = Metar.Metar(metar)
    airport = AIRPORT_INFO[metar.station_id]
    parts = []

    # intro
    template = '[$airport ATIS] [$letter] $time'
    part = Template(template).substitute(
        airport=metar.station_id,
        letter=atiscode,
        time=metar.time.strftime("%H%M"))
    parts.append(part)

    # expected approach
    template = '[EXP ${approach} APCH] [RWY IN USE] ${rwy}'
    part = Template(template).substitute(
        rwy=arrrwy,
        approach=airport['approaches'][arrrwy]
    )
    parts.append(part)

    # transition level
    template = '[TL] %s'
    transition_alt = airport['transition_altitude']
    index = bisect_right(
        TRANSITION_LEVEL[transition_alt],
        (metar.press._value,))
    _, transition_level = TRANSITION_LEVEL[transition_alt][index]
    parts.append(template % transition_level)

    # wind
    template = '[WND] ${direction} [DEG] ${speed} [KT]'
    part = Template(template).substitute(
        direction='%03d' % metar.wind_dir._degrees,
        speed='%d' % metar.wind_speed._value
    )
    parts.append(part)
    ## gusts
    if metar.wind_gust:
        template = '[MAX] ${gusts} [KT]'
        part = Template(template).substitute(
            gusts='%d' % metar.wind_gust._value
        )
        parts.append(part)
    ## variable
    if metar.wind_dir_to and metar.wind_dir_from:
        template = '[VRB BTN] ${from} [AND] ${to} [DEG]'
        part = Template(template).substitute(
            direction_from='%03d' % metar.wind_dir_from._degrees,
            direction_to='%03d' % metar.wind_dir_to._degrees
        )
        parts.append(part)

    # visibility
    if str(metar.vis) == 'greater than 10000 meters':
        parts.append('[VIS] [10KM]')

    for sky in metar.sky:
        cover, height, cb = sky
        parts.append('[%s] {%d} [FT]' % (cover, height._value))
        if cb:
            parts.append('CB')

    # temperature
    parts.append('[TEMP] %d' % metar.temp._value)

    # dewpoint
    parts.append('[DP] %d' % metar.dewpt._value)

    # QNH
    parts.append('[QNH] %d' % metar.press._value)

    parts.append('[ACK INFO] [%s]' % atiscode)

    return ' '.join(parts)
