"""
Message Maker

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>
                    Bernardo Reis

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

LPPT = {
    'approaches': {
        '03': 'ILS',
        '21': 'ILS Z',
        '35': 'VOR',
        '17': 'VISUAL'
    },
    'arrdep_info': {
        '03': [
            '[AFTER LANDING VACATE VIA HN]'
        ],
        '21': [
            '[AFTER LANDING VACATE VIA HS]',
            '[MEDIUM AND LIGHT AIRCRAFT EXPECT POSITION U FOR DEPARTURE, IF \
UNABLE ADVISE BEFORE TAXI]',
        ]
    },
    'general_info': [
        '[COMPLY WITH SPEED LIMITATIONS UNLESS OTHERWISE ADVISED BY ATC]'
    ],
    'transition_altitude': '4000'
}

AIRPORTS = {
    'LPPT': LPPT
}
