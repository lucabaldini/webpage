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


class LaTeX:

    """Small container class for LaTeX formatting.

    This is implemented as an "empty" class with a bunch of staticmethods and/or
    classemthods where appropriate.
    """

    @staticmethod
    def command(name: str, *args: str) -> str:
        """Basic function producing the text for LaTeX commands.

        Parameters
        ----------
        name : str
            The name of the command without the leading backslash
            (e.g., "emph").
        args : str
            The command arguments.

        Returns
        -------
        text : str
            The text of the LaTeX command.
        """
        text = '\\{}{}'.format(name, '{{{}}}' * len(args))
        return text.format(*args)

    @classmethod
    def emph(cls, text: str) -> str:
        """Italic formatting.
        """
        return cls.command('emph', text)

    @classmethod
    def bold(cls, text: str) -> str:
        """Bold formatting.
        """
        return cls.command('textbf', text)

    @classmethod
    def typeset(cls, text: str) -> str:
        """Typewriter formatting.
        """
        return cls.command('texttt', text)

    @classmethod
    def hyperlink(cls, text: str, url: Optional[str] = None) -> str:
        """Hyperlink formatting.

        If the url is None, this falls back to plain text.
        """
        if url is None:
            return text
        return cls.command('href', url, text)



class HTML:

    """Small container class for HTML formatting.

    This is implemented in the very same fashion as the LaTeX class.
    """

    INDENT_STRING = '  '

    @classmethod
    def indent(cls, text: str, level: int = 0) -> str:
        """Small utility function indent full paragraphs.

        This is essentially replacing any newline character prepending to it the
        proper number of spaces.
        """
        # If no indentation is required, do nothing.
        if level == 0:
            return text
        # Calculate the indentation.
        indent = cls.INDENT_STRING * level
        # Prepend the right number of spaces to each new line.
        text = text.replace('\n', '\n{}'.format(indent))
        # Prepend the right number of spaces to the paragraph itself.
        text = '{}{}'.format(indent, text)
        return text

    @classmethod
    def tag_open(cls, tag: str, indent: int = 0, class_: Optional[str] = None,
                 **attributes) -> str:
        """Open tag formatting.
        """
        if class_ is not None:
            attributes.update({'class': class_})
        attr_list = [' {}="{}"'.format(*item) for item in attributes.items()]
        attr_text = ','.join(attr_list)
        text = '<{}{}>'.format(tag, attr_text)
        return cls.indent(text, indent)

    @classmethod
    def tag_close(cls, tag: str, indent: int = 0) -> str:
        """Close tag formatting.
        """
        text = '</{}>'.format(tag)
        return cls.indent(text, indent)

    @classmethod
    def tag(cls, text: str, tag: str, indent: int = 0, class_: str = None,
            **attributes) -> str:
        """Formatting facility for a generic tag.

        Note that we factor the class attribute out of the keyword arguments
        because, while often needed in css, class is a reserved word in Python
        and cannot be passed directly as a key (we would have to build a
        dictionary manually every time).
        """
        return '{}{}{}'.format(cls.tag_open(tag, indent, class_, **attributes),
                               text, cls.tag_close(tag))

    @classmethod
    def heading3(cls, text: str, indent: int = 0, class_: str = None,
                 **attributes) -> str:
        """H3 tag.
        """
        return cls.tag(text, 'h3', indent, class_, **attributes)

    @staticmethod
    def break_() -> str:
        """Line break.
        """
        return '<br>'

    @classmethod
    def emph(cls, text: str, indent: int = 0, class_: str = None,
             **attributes) -> str:
        """Italic formatting.
        """
        return cls.tag(text, 'em', indent, class_, **attributes)

    @classmethod
    def bold(cls, text: str, indent: int = 0, class_: str = None,
             **attributes) -> str:
        """Bold formatting.
        """
        return cls.tag(text, 'b', indent, class_, **attributes)

    @classmethod
    def italic(cls, text: str = '', indent: int = 0, class_: str = None,
               **attributes) -> str:
        """Italic formatting.

        Mind in HTML 5 this is customarily used for other inline elements, such
        as icons.
        """
        return cls.tag(text, 'i', indent, class_, **attributes)

    @classmethod
    def typeset(cls, text: str, indent: int = 0, class_: str = None,
                **attributes) -> str:
        """Monospace formatting.
        """
        return cls.tag(text, 'tt', indent, class_, **attributes)

    @classmethod
    def list_item(cls, text: str, indent: int = 0, class_: str = None,
                  **attributes) -> str:
        """List item formatting.
        """
        return cls.tag(text, 'li', indent, class_, **attributes)

    @classmethod
    def list(cls, items: List, indent: int = 0, ul_class: Optional[str] = None,
             li_class: Optional[str] = None) -> str:
        """List formatting.

        Note that this function provides a minimal support for list
        customization through the ul_class and li_class arguments, but fancier
        formatting (e.g., where different list items have different attributes)
        are not supported.
        """
        lines = [cls.tag_open('ul', indent, ul_class)]
        for item in items:
            lines.append('{}'.format(cls.list_item(item, indent + 1, li_class)))
        lines.append(cls.tag_close('ul', indent))
        return '\n'.join(lines)

    @classmethod
    def hyperlink(cls, text: str, url: Optional[str] = None,
                  indent: int = 0) -> str:
        """Hyperlink formatting.

        If the url is None, this falls back to plain text.
        """
        if url is None:
            return text
        return cls.tag(text, 'a', indent, href=url)



class PageMenuEntry:

    """Class describing a page menu entry.

    Parameters
    ----------
    title : str
        The title for the menu entry (i.e., the text appearing in the menu)
    target : str
        The remote menu target (i.e., the page or folder the entry is pointing)
    icon : str
        The name of the (optional) icon associated to the menu entry.
    hook : function, optional
        An optional hook to dynamically add page content.


    A menu entry is the combination of a title and a target (to be intended in
    the remote server sense). Additionally, an optional function returning a
    string can be passed to the costructor to add dynamically generated text.
    (The output of the function is added verbatim to the corresponding page.)
    """

    def __init__(self, title: str, target: str, icon: Optional[str] = None,
                 hook=None, language: str = 'en') -> None:
        """Constructor.
        """
        self.title = title
        self.target = target
        self.icon = icon
        self.hook = hook
        self.language = language

    def points_to_file(self) -> bool:
        """Return True if the target is a html file name (i.e., not a folder).
        """
        return self.target.endswith('.html')

    def target_file_path(self, folder: str) -> Optional[str]:
        """Convert the raw target into a file path, prepending the folder
        passed as an argument.

        Return None is the target is not a file.
        """
        if not self.points_to_file():
            return None
        return os.path.join(folder, self.target)

    def ascii(self) -> str:
        """ASCII formatting.
        """
        return '{} -> {}'.format(self.title, self.target)

    def html(self, link_active: bool, indent: int) -> str:
        """HTML formatting.
        """
        if link_active:
            text = HTML.hyperlink(self.title, self.target)
            class_ = 'active'
        else:
            text = self.title
            class_ = 'inactive'
        if self.icon is not None:
            text = '{}{}'.format(HTML.italic(class_=self.icon), text)
        return HTML.list_item(text, indent, class_=class_)

    def __str__(self) -> str:
        """String formatting.
        """
        return self.ascii()



class PageMenu(List[PageMenuEntry]):

    """Class representing the logical structure of the page menu.

    A menu is essentially a list of PageMenuEntry instances.
    """

    def add_entry(self, title: str, target: str, icon: Optional[str] = None,
                  hook=None, language: str = 'en') -> None:
        """Add an entry to the menu.
        """
        self.append(PageMenuEntry(title, target, icon, hook, language))

    def ascii(self) -> str:
        """ASCII representation.
        """
        lines = ['Page menu:']
        for entry in self:
            lines.append(entry.ascii())
        return '\n'.join(lines)

    def html(self, current_title: Optional[str] = None) -> str:
        """Return the html representation of the menu.
        """
        lines = ['<ul>']
        for entry in self:
            link_active = (entry.title != current_title)
            lines.append(entry.html(link_active, 1))
        lines.append('</ul>')
        return '\n'.join(lines)

    def __str__(self) -> str:
        """Text representation.
        """
        return self.ascii()



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

    @staticmethod
    def date_to_str(date: datetime.date, month: bool = True,
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

    def ascii(self) -> str:
        """ASCII formatting.
        """
        return self.__format('--')

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
        return self.ascii()



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

    def ascii(self) -> str:
        """ASCII formatting.
        """
        text = '{}'.format(self.title)
        if self.notes:
            text += ' ({})'.format(self.notes)
        elif self.invited:
            text += ' (invited talk)'
        elif self.poster:
            text += ' (poster)'
        return text

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
        return self.ascii()



class Conference:

    """Class describing a conference.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, name: str, location: str, webpage: str,
                 begin: str, end: Optional[str] = None) -> None:
        """Constructor.
        """
        self.name = name
        self.location = location
        self.webpage = webpage
        self.time_span = TimeSpan(begin, end)
        self.contributions: List[Contribution] = []

    def add_contribution(self, title: str, invited: bool = False,
                         poster: bool = False, notes: Optional[str] = None):
        """Add a contribution to the conference.

        Mind this is returning the conference object itself so that multiple
        additions can be chained.
        """
        contribution = Contribution(title, invited, poster, notes)
        self.contributions.append(contribution)
        return self

    def year(self) -> int:
        """Return thr year of the conference.
        """
        return self.time_span.begin_date.year

    def ascii(self) -> str:
        """ASCII formatting.
        """
        text = '{}, {}, {}'.format(self.name, self.location, self.time_span)
        for contribution in self.contributions:
            text = '{}\n- {}'.format(text, contribution)
        return text

    def html(self, indent: int = 0) -> str:
        """HTML formatting.

        Mind we're passing an additional indentation argument to the function,
        here, because otherwise it would be impossible to have the single
        contributions lined up properly. Not the most elegant thing in the
        world, admittedly.
        """
        if self.webpage is not None:
            text = '<a href="{}">{}</a>'.format(self.webpage, self.name)
        else:
            text = self.name
        text = '{}, {}, {}'.format(text, self.location, self.time_span.html())
        for contribution in self.contributions:
            contr = HTML.indent(contribution.html(), indent + 1)
            text = '{}{}\n{}'.format(text, HTML.break_(), contr)
        return text

    def latex(self) -> str:
        """LaTeX formatting.

        Warning
        -------
        Need to add the loop over the contributions.
        """
        if self.webpage is not None:
            text = '\\href{{{}}}{{{}}}'.format(self.webpage, self.name)
        else:
            text = self.name
        text += ', {}, {}'.format(self.location, self.time_span.latex())
        return text

    def __str__(self) -> str:
        """String formatting.
        """
        return self.ascii()



class ConferenceList(list):

    """Class describing a list of conferences.
    """

    # pylint: disable=too-many-arguments
    def add_conference(self, name: str, location: str, webpage,
                       begin: str, end: Optional[str] = None) -> Conference:
        """Add a conference to the conference list.
        """
        conference = Conference(name, location, webpage, begin, end)
        self.append(conference)
        return conference

    def html(self, indent: int = 4) -> str:
        """HTML formatting.
        """
        lines = [HTML.tag_open('ul', indent, class_='conference-list')]
        current_year = None
        for i, conference in enumerate(self):
            if conference.year() != current_year:
                class_ = 'conference-year'
                lines.append(HTML.list_item(conference.year(), indent + 1, class_))
                current_year = conference.year()
            class_ = 'conference-item'
            text = '[{}] {}'.format(i + 1, conference.html(indent + 1))
            lines.append(HTML.list_item(text, indent + 1, class_))
        lines.append(HTML.tag_close('ul', indent))
        return '\n'.join(lines)
