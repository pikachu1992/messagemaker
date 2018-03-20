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
from flask import Flask, request
from messagemaker import atis
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    metar = request.args.get('metar')
    rwy = request.args.get('rwy')
    letter = request.args.get('letter')

    if metar and rwy and letter:
        return atis.message_try(metar, rwy, letter)
    else:
        return 'wrong usage'

if __name__ == '__main__':
    if 'PORT' in os.environ:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
    else:
        app.run()
