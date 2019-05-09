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

"""Test suite for the core module.
"""

import unittest

from typing import Optional

from .context import core



class TestTimeSpan(unittest.TestCase):

    """Unit tests for the TimeSpan class.
    """

    def _test(self, begin: str, end: Optional[str] = None,
              single_day: bool = False):
        """Basic test worker.
        """
        span = core.TimeSpan(begin, end)
        print(span)
        print(span.html())
        print(span.latex())
        self.assertEqual(span.is_single_day(), single_day)

    def test_basic(self):
        """Test the normal constructor.
        """
        self._test('1977-04-05', '2019-05-10', False)

    def test_single_day(self):
        """Test the normal constructor with a one-day interval.
        """
        self._test('1977-04-05', '1977-04-05', True)

    def test_single_argument(self):
        """Test the begin-only constructor.
        """
        self._test('1977-04-05', single_day=True)



class TestContribution(unittest.TestCase):

    """Unit tests for the Contribution class.
    """

    def _test(self, title: str, invited: bool = False, poster: bool = False,
              notes: Optional[str] = None):
        """Basic test worker.
        """
        contribution = core.Contribution(title, invited, poster, notes)
        print(contribution)
        print(contribution.html())
        print(contribution.latex())

    def test_basic(self):
        """Basic test.
        """
        self._test('My paper title')

    def test_invited(self):
        """Invited talk.
        """
        self._test('My paper title', invited=True)

    def test_poster(self):
        """Invited talk.
        """
        self._test('My paper title', poster=True)

    def test_notes(self):
        """Test a contribution with notes.
        """
        self._test('Lecture', invited=True, notes='Series of invited lectures')



class TestConference(unittest.TestCase):

    """Unit tests for the Conference class.
    """

    def test_basic(self):
        """Test the plain constructor.
        """
        conference = core.Conference('A conference', 'San Diego',
                                     '2012-04-16', '2012-04-17',
                                     'www.conference.us')
        print(conference)
        print(conference.html())
        print(conference.latex())



if __name__ == '__main__':
    unittest.main()
