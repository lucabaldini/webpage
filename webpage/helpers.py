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

"""Utility functions.
"""


from typing import Optional



class LaTeX:

    """Small container class for LaTeX formatting.
    """

    @classmethod
    def emph(cls, text: str) -> str:
        """Italic formatting.
        """
        return '\\emph{{{}}}'.format(text)

    @classmethod
    def bold(cls, text: str) -> str:
        """Bold formatting.
        """
        return '\\texttt{{{}}}'.format(text)

    @classmethod
    def typeset(cls, text: str) -> str:
        """Monospace formatting.
        """
        return '\\textbf{{{}}}'.format(text)

    @classmethod
    def hyperlink(cls, text: str, url: Optional[str] = None) -> str:
        """Hyperlink
        """
        if url is None:
            return text
        return '\\href{{{}}}{{{}}}'.format(url, text)



class HTML:

    """Small container class for HTML formatting.
    """

    INDENT_STRING = ' ' * 2

    @classmethod
    def indent(cls, text: str, level: int = 0) -> str:
        """Indentation facility.
        """
        # TO be implemented.
        return ''

    @classmethod
    def _tag(cls, text: str, tag: str, **attributes: dict) -> str:
        """Formatting facility for a generic tag.
        """
        attr_list = [' {}="{}"'.format(*item) for item in attributes.items()]
        attr_text = ','.join(attr_list)
        return '<{0}{1}>{2}</{0}>'.format(tag, attr_text, text)

    @classmethod
    def emph(cls, text: str) -> str:
        """Italic formatting.
        """
        return cls._tag(text, 'em')

    @classmethod
    def bold(cls, text: str) -> str:
        """Bold formatting.
        """
        return cls._tag(text, 'b')

    @classmethod
    def typeset(cls, text: str) -> str:
        """Monospace formatting.
        """
        return cls._tag(text, 'tt')

    @classmethod
    def hyperlink(cls, text: str, url: Optional[str] = None) -> str:
        """Hyperlink
        """
        if url is None:
            return text
        attributes = dict(href=url)
        return cls._tag(text, 'a', **attributes)
