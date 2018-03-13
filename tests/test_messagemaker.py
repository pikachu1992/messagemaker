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
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_messagemaker
----------------------------------

Tests for `messagemaker` module.
"""

import unittest
from ddt import ddt, data

from messagemaker import message


@ddt
class TestMessageMaker(unittest.TestCase):

    def test_makeSubstitute_primative_returnsSelf(self):
        format = '$test'
        context = {
            'test': 'true'
        }
        result = message.make_substitute(format, context)
        self.assertEqual(result, 'true')
