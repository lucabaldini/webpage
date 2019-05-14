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


from typing import Optional, List



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
    def tag(cls, text: str, tag: str, indent: int = 0, **attributes) -> str:
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
        return cls.tag(text, 'em', indent)

    @classmethod
    def bold(cls, text: str, indent: int = 0) -> str:
        """Bold formatting.
        """
        return cls.tag(text, 'b', indent)

    @classmethod
    def typeset(cls, text: str, indent: int = 0) -> str:
        """Monospace formatting.
        """
        return cls.tag(text, 'tt', indent)

    @classmethod
    def list_item(cls, text: str, indent: int = 0) -> str:
        """List item formatting.
        """
        return cls.tag(text, 'li', indent)

    @classmethod
    def list(cls, items: List) -> str:
        """List formatting.
        """
        lines = ['<ul>\n']
        for item in items:
            lines.append('{}\n'.format(cls.list_item(item, indent=1)))
        lines.append('</ul>')
        return ''.join(lines)

    @classmethod
    def hyperlink(cls, text: str, url: Optional[str] = None,
                  indent: int = 0) -> str:
        """Hyperlink formatting.

        If the url is None, this falls back to plain text.
        """
        if url is None:
            return text
        return cls.tag(text, 'a', indent, href=url)
