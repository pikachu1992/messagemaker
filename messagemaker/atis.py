"""
Message Maker

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

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
import requests


def message_try(metar, rwy, letter):
    response = None
    try:
        response = message(metar, rwy, letter)
    except Exception as crap:
        print(crap)

    return '[ATIS OUT OF SERVICE]' if response is None else response

def message(metar, rwy, letter):
    if len(metar) == 4:
        metar = download_metar(metar)

    metar = Metar.Metar(metar)
    airport = AIRPORT_INFO[metar.station_id]
    parts = []

    # intro
    template = '[$airport ATIS] [$letter] $time'
    part = Template(template).substitute(
        airport=metar.station_id,
        letter=letter,
        time=metar.time.strftime("%H%M"))
    parts.append(part)

    # expected approach
    template = '[EXP ${approach} APCH] [RWY IN USE ${rwy}]'
    part = Template(template).substitute(
        rwy=rwy,
        approach=airport['approaches'][rwy]
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

    # specific departure and arrival information
    for rwy_message in airport['arrdep_info'][rwy]:
        parts.append(rwy_message)

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
        template = '[VRB BTN] ${direction_from} [AND] ${direction_to} [DEG]'
        part = Template(template).substitute(
            direction_from='%03d' % metar.wind_dir_from._degrees,
            direction_to='%03d' % metar.wind_dir_to._degrees
        )
        parts.append(part)

    # sky conditions
    print(metar.vis)
    if str(metar.vis) == '10000 meters':
        parts.append('[CAVOK]')
    else:
        ## visibility
        if str(metar.vis) == 'greater than 10000 meters':
            parts.append('[VIS] 10[KM]')
        ## clouds
        if 'sky' in metar.sky:
            parts.append('[CLD]')
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

    # general arrival and departure information
    for general_info in airport['general_info']:
        parts.append(general_info)

    parts.append('[ACK %s INFO] [%s]' % (metar.station_id.upper(), letter))

    return ' '.join(parts)

def download_metar(icao):
    return requests.get(
        'https://avwx.rest/api/metar/%s' % icao).json()['Raw-Report']
