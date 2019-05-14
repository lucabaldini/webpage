# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Luca Baldini (luca.baldini@pi.infn.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Test suite for the helpers module.
"""

import unittest

from .context import helpers


class TestHTML(unittest.TestCase):

    """Unit tests for the TimeSpan class.
    """

    def test_base(self, text:str = 'Hello world!'):
        """Basic tests of the HTML tags.
        """
        source = helpers.HTML.emph(text)
        target = '<em>{}</em>'.format(text)
        self.assertEqual(source, target)
        source = helpers.HTML.bold(text)
        target = '<b>{}</b>'.format(text)
        self.assertEqual(source, target)
        source = helpers.HTML.typeset(text)
        target = '<tt>{}</tt>'.format(text)
        self.assertEqual(source, target)




if __name__ == '__main__':
    unittest.main()
