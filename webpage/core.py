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
import os

from typing import Optional, List

from webpage.helpers import HTML


class PageMenu(dict):

    """Class representing the logical structure of the page menu.

    A menu is a essentially a series of entries, each of which includes a
    title and a target. The title is the title of the web page, while the
    target can either be a html file or a folder, and is always intented to
    be in the (remote, or relative) html space.

    Note that the class is inheriting from dict and the fact that the entries
    are expected to appear in order in the output html relies on the fact that
    dictionaries are now guaranteed to preserve the insertion order in
    Python.
    """

    def add_entry(self, title: str, target: str) -> None:
        """Add an entry to the menu.
        """
        self[title] = target

    def target(self, title: str) -> str:
        """Return the target corresponding to a given title.
        """
        return self.get(title)

    @classmethod
    def target_is_file(cls, target: str) -> bool:
        """Return True if the given target represents a html file name
        (i.e., not a folder).
        """
        return target.endswith('.html')

    def target_points_to_file(self, title: str) -> bool:
        """Return True if the target corresponding to the given title represents
        a html file name (i.e., not a folder).
        """
        return self.target_is_file(self.target(title))

    def target_file_path(self, title: str, folder: str) -> Optional[str]:
        """Convert the raw target into a file path, prepending the folder
        passed as an argument.

        Return None is the target is not a file.
        """
        target = self.target(title)
        if not self.target_is_file(target):
            return None
        return os.path.join(folder, target)

    def to_html(self, current_page_title: Optional[str] = None) -> str:
        """Return the html representation of the menu.
        """
        lines = ['<ul>']
        for title, target in self.items():
            if title == current_page_title:
                # Funny: we can't pass this as a keyword argument, as class
                # is a reserved word :-)
                attr = {'class': 'current'}
                lines.append(HTML.list_item(title, 1, **attr))
            else:
                lines.append(HTML.list_item(HTML.hyperlink(title, target), 1))
        lines.append('</ul>')
        return '\n'.join(lines)

    def __str__(self) -> str:
        """Text representation.
        """
        text = 'Page menu:\n'
        for title, target in self.items():
            text += '- %s -> %s\n' % (title, target)
        return text



class TimeSpan:

    """Small utility class representing a time span.

    This is used for expressing the time duration of conferences, and its main
    purpose is to make the magic that renders 2--8 April and 28 April--3 May
    automagically.

    The begin and end strings should be expressed in iso format 'YYYY-MM-DD'.
    If the optional end string is None, it is assumed that the begin and end
    dates are identical and the time span is one-day long.
    """

    INPUT_FMT = '%Y-%m-%d'

    def __init__(self, begin: str, end: Optional[str] = None) -> None:
        """Constructor.
        """
        if end is None:
            end = begin
        self.begin_date = self.str_to_date(begin)
        self.end_date = self.str_to_date(end)
        # Make sure we did not get the bounds backward.
        assert self.end_date >= self.begin_date

    @classmethod
    def str_to_date(cls, string: str) -> datetime.date:
        """Convert an input string to a datetime.date object.
        """
        return datetime.datetime.strptime(string, cls.INPUT_FMT).date()

    @classmethod
    def date_to_str(cls, date: datetime.date, month: bool = True,
                    year: bool = True) -> str:
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
            fmt += ', %Y'
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
        return '{}{}{}'.format(begin, separator, end)

    def html(self) -> str:
        """HTML formatting.
        """
        return self.__format('&ndash;')

    def latex(self) -> str:
        """LaTeX formatting.
        """
        return self.__format('--')

    def __str__(self) -> str:
        """String formatting.
        """
        return self.__format('--')



class Contribution:

    """Class describing a conference contribution (i.e., a talk or a poster).
    """

    def __init__(self, title: str, invited: bool = False, poster: bool = False,
                 notes: Optional[str] = None) -> None:
        """
        """
        self.title = title
        self.invited = invited
        self.poster = poster
        self.notes = notes

    def html(self) -> str:
        """HTML formatting.
        """
        text = '<em>"{}"</em>'.format(self.title)
        if self.notes:
            text += ' (<b>{}</b>)'.format(self.notes)
        elif self.invited:
            text += ' (<b>invited talk</b>)'
        elif self.poster:
            text += ' (poster)'
        return text

    def latex(self) -> str:
        """LaTeX formatting.
        """
        text = '"\\emph{{{}}}"'.format(self.title)
        if self.notes:
            text += ' ({{\\bfseries {}}})'.format(self.notes)
        elif self.invited:
            text += ' ({\\bfseries invited talk})'
        elif self.poster:
            text += ' (poster)'
        return text

    def __str__(self) -> str:
        """String formatting.
        """
        text = '{}'.format(self.title)
        if self.notes:
            text += ' ({})'.format(self.notes)
        elif self.invited:
            text += ' (invited talk)'
        elif self.poster:
            text += ' (poster)'
        return text



class Conference:

    """Class describing a conference.
    """

    def __init__(self, name: str, location: str, begin: str,
                 end: Optional[str] = None,
                 webpage: Optional[str] = None) -> None:
        """Constructor.
        """
        self.name = name
        self.location = location
        self.time_span = TimeSpan(begin, end)
        self.webpage = webpage
        self.contributions: List[Contribution] = []

    def add_contribution(self, contribution: Contribution):
        """Add a contribution to the conference.

        Mind this is returning the conference object itself so that multiple
        additions can be chained.
        """
        self.contributions.append(contribution)
        return self

    def html(self) -> str:
        """HTML formatting.
        """
        if self.webpage is not None:
            text = '<a href="{}">{}</a>'.format(self.webpage, self.name)
        else:
            text = self.name
        text += ', {}, {}'.format(self.location, self.time_span)
        return text

    def latex(self) -> str:
        """LaTeX formatting.
        """
        if self.webpage is not None:
            text = '\\href{{{}}}{{{}}}'.format(self.webpage, self.name)
        else:
            text = self.name
        text += ', {}, {}'.format(self.location, self.time_span)
        return text

    def __str__(self) -> str:
        """String formatting.
        """
        return '{}, {}, {}'.format(self.name, self.location, self.time_span)
