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
        """Hyperlink formatting.

        If the url is None, this falls back to plain text.
        """
        if url is None:
            return text
        return '\\href{{{}}}{{{}}}'.format(url, text)



class HTML:

    """Small container class for HTML formatting.
    """

    INDENT_STRING = '  '

    @classmethod
    def indent(cls, text: str, level: int = 0) -> str:
        """Small utility function indent full paragraphs.

        This is essentially replacing any newline character prepending to it the
        proper number of spaces.
        """
        # Calculate the indentation.
        indent = cls.INDENT_STRING * level
        # Prepend the right number of spaces to each new line.
        text = text.replace('\n', '\n{}'.format(indent))
        # Prepend the right number of spaces to the paragraph itself.
        text = '{}{}'.format(indent, text)
        return text

    @classmethod
    def tag(cls, text: str, tag: str, indent: int = 0,
            **attributes: dict) -> str:
        """Formatting facility for a generic tag.
        """
        attr_list = [' {}="{}"'.format(*item) for item in attributes.items()]
        attr_text = ','.join(attr_list)
        text = '<{0}{1}>{2}</{0}>'.format(tag, attr_text, text)
        return cls.indent(text, indent)

    @classmethod
    def emph(cls, text: str, indent: int = 0) -> str:
        """Italic formatting.
        """
        text = cls.tag(text, 'em')
        return cls.indent(text, indent)

    @classmethod
    def bold(cls, text: str, indent: int = 0) -> str:
        """Bold formatting.
        """
        text = cls.tag(text, 'b')
        return cls.indent(text, indent)

    @classmethod
    def typeset(cls, text: str, indent: int = 0) -> str:
        """Monospace formatting.
        """
        text = cls.tag(text, 'tt')
        return cls.indent(text, indent)

    @classmethod
    def hyperlink(cls, text: str, url: Optional[str] = None,
                  indent: int = 0) -> str:
        """Hyperlink formatting.

        If the url is None, this falls back to plain text.
        """
        if url is None:
            return text
        attributes = dict(href=url)
        text = cls.tag(text, 'a', **attributes)
        return cls.indent(text, indent)
