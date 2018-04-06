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
    'transition_altitude': '4000',
    'clrfreqs': (
        # freq, contact message, closed message
        (118.95, 'FOR DEPARTURE CLEARANCE CONTACT DEL 118.950', 'DEL CLOSED'),
        (121.75, 'DEL FREQ CLOSED FOR DEPARTURE CLEARANCE CONTACT GND 121.750'),
        (118.1, 'GND AND DEL FREQ CLOSED FOR DEPARTURE CLEARANCE CONTACT \
TWR 118.100'),
        (119.1, 'ON THE GROUND CONTACT 119.100'),
        (125.55, 'ON THE GROUND CONTACT 125.550'),
    ),
    'depfreqs': (
        (125.125, 'AFTER DEPARTURE CONTACT 125.125'),
        (119.1, 'AFTER DEPARTURE CONTACT 119.1'),
        (125.55, 'AFTER DEPARTURE CONTACT 125.55'),
    ),
}
LPFR = {
    'approaches': {
        '10': 'R-NAV', # é substituído em [EXP <aqui> APCH]
        '28': 'ILS'
    },
    'arrdep_info': {
        '10': [],
        '28': []
    },
    'general_info': [],
    'transition_altitude': '4000'
}
LPPR = {
    'approaches': {
        '17': 'ILS DME', # é substituído em [EXP <aqui> APCH]
        '35': 'R-NAV'
    },
   'arrdep_info': {
        '17': [],
        '35': []
    },
    'general_info': [],
    'transition_altitude': '4000'
}
LPMA = {
    'approaches': {
        '05': 'VOR DME', # é substituído em [EXP <aqui> APCH]
        '23': 'VOR DME'
    },
    'arrdep_info': {
        '05': [],
        '23': []
    },
    'general_info': [],
    'transition_altitude': '5000'
}

AIRPORTS = {
    'LPPT': LPPT,
    'LPFR': LPFR,
    'LPPR': LPPR,
    'LPMA': LPMA
}

TRANSITION = {
    '4000': [
        (942.1, '75'),
        (959.4, '70'),
        (977.1, '65'),
        (995.0, '60'),
        (1013.2, '55'),
        (1031.6, '50'),
        (1050.3, '45'),
        (9999, '40')
    ],
    '5000': [
        (942.1, '85'),
        (959.4, '80'),
        (977.1, '75'),
        (995.0, '70'),
        (1013.2, '65'),
        (1031.6, '60'),
        (1050.3, '55'),
        (9999, '50')
    ],
    '6000': [
        (942.1, '95'),
        (959.4, '90'),
        (977.1, '85'),
        (995.0, '80'),
        (1013.2, '75'),
        (1031.6, '70'),
        (1050.3, '65'),
        (9999, '60')
    ],
    '8000': [
        (942.1, '115'),
        (959.4, '110'),
        (977.1, '105'),
        (995.0, '100'),
        (1013.2, '95'),
        (1031.6, '90'),
        (1050.3, '85'),
        (9999, '80')
    ]
}
