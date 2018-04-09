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
import json
import traceback

def message_try(metar, rwy, letter, airports, tl_tbl):
    response = None
    try:
        response = message(metar, rwy, letter, airports, tl_tbl)
    except Exception as crap:
        print(traceback.format_exc())

    return '[ATIS OUT OF SERVICE]' if response is None else response

def clrfreq(airport, online_freqs):
    if len(online_freqs) < 2:
        return None
    
    parts = airport['clr_freq']
    for freq, part in parts:
        if freq in online_freqs:
            return part

def intro(letter, metar):
    template = '[$airport ATIS] [$letter] $time'
    return Template(template).substitute(
        airport=metar.station_id,
        letter=letter,
        time=metar.time.strftime("%H%M"))

def approach(rwy, airport):
    template = '[EXP ${approach} APCH] [RWY IN USE ${rwy}]'
    return Template(template).substitute(
        rwy=rwy,
        approach=airport['approaches'][rwy])

def transition_level(airport, tl_tbl, metar):
    template = '[TL] %s'
    transition_alt = airport['transition_altitude']
    index = bisect_right(
        tl_tbl[transition_alt],
        (metar.press._value,))
    _, transition_level = tl_tbl[transition_alt][index]
    return template % transition_level

def arrdep_info(airport, rwy):
    if rwy not in airport['arrdep_info']:
        return ''
    parts = []
    for rwy_message in airport['arrdep_info'][rwy]:
        parts.append(rwy_message)
    return ' '.join(parts)

def wind(metar):
    parts = []
    if metar.wind_dir:
        template = '[WND] ${direction} [DEG] ${speed} [KT]'
        part = Template(template).substitute(
            direction='%03d' % metar.wind_dir._degrees,
            speed='%d' % metar.wind_speed._value)

        # calm winds (to avoid WND 000 DEG 0 KT)
        if metar.wind_speed._value == 0:
            parts.append('[WND] [CALM]')
        else:
            parts.append(part)
    else:
        parts.append('[WND] [VRB] %d [KT]' % metar.wind_speed._value)
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
    return ' '.join(parts)

def precip(metar):
    if not metar.weather:
        return ''

    parts = []
    for weather in metar.weather:
        intensity, description, precipitation, obscuration, other = weather

        # do the intensity of the precipitation first
        if intensity is not None and precipitation:
            if intensity == '':
                parts.append('[MOD]')
            elif intensity == '-':
                parts.append('[FBL]')
            elif intensity == '+':
                parts.append('[HVY]')

        joint_part = []
        if precipitation:
            if description:
                joint_part.append(description)
            joint_part.append(precipitation)
            if len(joint_part) > 0:
                parts.append('[%s]' % ''.join(joint_part))

        if obscuration:
            if description:
                joint_part.append(description)
            joint_part.append(obscuration)
            if len(joint_part) > 0:
                parts.append('[%s]' % ''.join(joint_part))

    return ' '.join(parts)

def sky(metar):
    parts = []
    if str(metar.vis) == '10000 meters':
        parts.append('[CAVOK]')
    else:
        ## visibility
        # above or at 5km visibility is given in KM:
        #   5KM 6KM 7KM .. 10KM
        # below 5 km visibility is given in meters:
        #   4000M 3000M ..
        if metar.vis:
            # calculate units, see issue #22
            vis = int(metar.vis._value)
            units = 'MTS'
            if metar.vis._value >= 5000:
                vis = int(metar.vis._value / 1000)
                units = 'KM'
            if vis % 100 == 0:
                vis = '{%d}' % vis
            parts.append('[VIS] %s[%s]' % (vis, units))
        ## clouds
        clouds = [c for c in metar.sky if c[0] in ('FEW', 'SCT', 'BKN', 'OVC')]
        if len(clouds) > 0:
            parts.append('[CLD]')
        for sky in metar.sky:
            cover, height, cb = sky
            parts.append('[%s]' % cover)
            if cb:
                parts.append('[%s]' % cb.upper())
            parts.append('{%d} [FT]' % height._value)
    return ' '.join(parts)

def temperature(metar):
    return '[TEMP] %d' % metar.temp._value

def dewpoint(metar):
    return '[DP] %d' % metar.dewpt._value

def qnh(metar):
    return '[QNH] %d' % metar.press._value

def message(metar, rwy, letter, airports, tl_tbl):
    if len(metar) == 4:
        metar = download_metar(metar)

    metar = Metar.Metar(metar)
    airport = airports[metar.station_id]
    parts = []

    parts.append(intro(letter, metar))
    parts.append(approach(rwy, airport))
    parts.append(transition_level(airport, tl_tbl, metar))
    parts.append(arrdep_info(airport, rwy))
    parts.append(wind(metar))
    parts.append(precip(metar))
    parts.append(sky(metar))
    parts.append(temperature(metar))
    parts.append(dewpoint(metar))
    parts.append(qnh(metar))

    # general arrival and departure information
    for general_info in airport['general_info']:
        parts.append(general_info)

    parts.append('[ACK %s INFO] [%s]' % (metar.station_id.upper(), letter))

    return ' '.join(parts)

def download_metar(icao):
    return requests.get(
        'https://avwx.rest/api/metar/%s' % icao).json()['Raw-Report']

def get_online_stations(icao):
    """Returns all vatsim frequencies online at
    a given airport"""

    url='https://vatsim-status-proxy.herokuapp.com/clients?where={"clienttype":\"ATC"}'
    data=json.loads(requests.get(url).text)
    return [c['frequency'] for c in data
            if icao in c['callsgn']]

