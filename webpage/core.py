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

"""Core logic for the website generation.
"""

import datetime

from typing import Optional


class Timespan:

    """Small utility class representing a time span.

    This is used for expressing the time duration of conferences, and its main
    purpose is to make the magic that renders 2--8 April and 28 April--3 May
    automagically.

    The begin and end strings should be expressed in iso format 'YYYY-MM-DD'.
    If the optional end string is None, it is assumed that the begin and end
    dates are identical and the time span is one-day long.
    """

    INPUT_FMT = '%Y-%m-%d'

    def __init__(self, begin: str, end: Optional[str] = None):
        """Constructor.
        """
        if end is None:
            end = begin
        self.begin_date = self.str_to_date(begin)
        self.end_date = self.str_to_date(end)
        # Make sure we did not get the bounds backward.
        assert(self.end_date >= self.begin_date)

    @classmethod
    def str_to_date(cls, string: str) -> datetime.date:
        """Convert an input string to a datetime.date object.
        """
        return datetime.datetime.strptime(string, cls.INPUT_FMT).date()

    @classmethod
    def date_to_str(cls, date: datetime.date, month: bool = True,
                    year: bool = True, year_comma: bool = True) -> str:
        """Format a datetime.date object to an output string.

        By default this returns the full date in the form of 05 April 1977,
        but the method is adding optional flexibility to suppress the year
        and/or the month, in order to be able to express time spans in a 
        human-readable format.
        """
        fmt = '%d'
        if month is True:
            fmt += ' %B'
        if year is True:
            if year_comma:
                fmt += ', %Y'
            else:
                fmt += ' %Y'
        return date.strftime(fmt)

    def is_single_day(self) -> bool:
        """Return true if the period spans a single day.
        """
        return self.begin_date == self.end_date

    def __format(self, separator: str = '--') -> str:
        """General-purpose string formatting for the Timestamp class.
        """
        if self.is_single_day():
            return self.date_to_str(self.begin_date)
        end = self.date_to_str(self.end_date)
        if self.begin_date.year != self.end_date.year:
            begin = self.date_to_str(self.begin_date)
        elif self.begin_date.month != self.end_date.month:
            begin = self.date_to_str(self.begin_date, year=False)
        else:
            begin = self.date_to_str(self.begin_date, month=False, year=False)
        return '%s%s%s' % (begin, separator, end)

    def html(self) -> str:
        """ HTML formatting.
        """
        return self.__format('&ndash;')

    def latex(self) -> str:
        """ LaTeX formatting.
        """
        return self.__format('--')

    def __str__(self) -> str:
        """String formatting.
        """
        return self.__format('--')
        


if __name__ == '__main__':
    s = Timespan('1977-05-10', '2019-05-10')
    print(s)
    print(s.html())
    print(s.latex())
    print(s.is_single_day())
    s = Timespan('1977-05-10', '1977-05-11')
    print(s)
    print(s.is_single_day())
    s = Timespan('1977-05-10')
    print(s)
    print(s.is_single_day())
