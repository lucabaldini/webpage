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

"""Module containing all the facilities for the static html generation.
"""

import datetime
import os
import shutil
import glob
import logging

from typing import Optional

from webpage.core import PageMenu


# Basic configuration.
#
PAGE_AUTHOR = 'Luca Baldini'
PAGE_DESCRIPTION = '%s\'s home page' % PAGE_AUTHOR
PAGE_BASE_TITLE = 'Luca Baldini @ UNIPI/INFN&ndash;Pisa'
PAGE_HEADER_TEXT = PAGE_BASE_TITLE
PAGE_KEYWORDS = ('Luca Baldini',
                 'INFN',
                 'University',
                 'Pisa',
                 'Physics',
                 'Astrophysics',
                 'Fermi',
                 'GLAST',
                 'IXPE')
PAGE_KEYWORDS_STRING = ', '.join(PAGE_KEYWORDS)
DATETIME_FORMAT = '%A, %B %d %Y at %H:%M'
LAST_UPDATE = datetime.datetime.now()
LAST_UPDATE_STRING = LAST_UPDATE.strftime(DATETIME_FORMAT)
COPYRIGHT_START_YEAR = 2012
COPYRIGHT_END_YEAR = LAST_UPDATE.year
INDENT_STRING = '  '
STYLE_SHEETS = ['default.css']
DEFAULT_STYLE_SHEET = STYLE_SHEETS[0]


# Basic remote environment.
#
REMOTE_CSS_FOLDER = 'css'
REMOTE_IMG_FOLDER = 'images'
DEFAULT_CSS_HREF = '%s/%s' % (REMOTE_CSS_FOLDER, DEFAULT_STYLE_SHEET)


# Basic local environment.
#
BASE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONTENTS_FOLDER = os.path.join(BASE_FOLDER, 'contents')
CSS_FOLDER = os.path.join(BASE_FOLDER, 'css')
IMG_FOLDER = os.path.join(BASE_FOLDER, 'images')
HTML_OUTPUT_FOLDER = os.path.join(BASE_FOLDER, 'html')
CSS_OUTPUT_FOLDER = os.path.join(HTML_OUTPUT_FOLDER, REMOTE_CSS_FOLDER)
IMG_OUTPUT_FOLDER = os.path.join(HTML_OUTPUT_FOLDER, REMOTE_IMG_FOLDER)


def create_local_tree():
    """Create the necessary local tree for the html output, if necessary.
    """
    for folder in [HTML_OUTPUT_FOLDER, CSS_OUTPUT_FOLDER, IMG_OUTPUT_FOLDER]:
        if not os.path.exists(folder):
            logging.info('Creating output folder %s...', folder)
            os.mkdir(folder)


def content_file_path(file_name: str) -> str:
    """Return the path to a content file path.
    """
    return os.path.join(CONTENTS_FOLDER, file_name)


def html_output_file_path(file_path: str) -> str:
    """Return the path to a generic output file path.
    """
    file_name = os.path.basename(file_path)
    return os.path.join(HTML_OUTPUT_FOLDER, file_name)


PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset=utf-8">
    <title>%s :: %%s</title>
    <meta name="keywords" content="%s">
    <meta name="description" content="%s">
    <meta name="author" content="%s">
    <link rel="stylesheet" href="%s" type="text/css" media="all">
  </head>

  <body>
    <div id="header">
      <h1>%s</h1>
    </div>

    <div id="container">
      <div id="menu">
%%s
      </div>
      <div id="contents">
        <h2>%%s</h2>
%%s
      </div>
    </div>

    <div id="footer">
%%s
    </div>
  </body>
</html>
""" % (PAGE_BASE_TITLE, PAGE_KEYWORDS_STRING, PAGE_DESCRIPTION, PAGE_AUTHOR,
       DEFAULT_CSS_HREF, PAGE_HEADER_TEXT)


FOOTER_TEMPLATE = """
Copyright &copy; %d&ndash;%d Luca Baldini
(<a href=about.html>about this website</a>).
The views expressed here are my personal views, not those of the
University of Pisa nor of INFN.<br>

For what it's worth, this page validates as
<a href="http://validator.w3.org/check?uri=referer">HTML 4.01 strict</a>
and
<a href="http://jigsaw.w3.org/css-validator/check/referer">css level 3</a>.<br>

Last update on %s.
""" % (COPYRIGHT_START_YEAR, COPYRIGHT_END_YEAR, LAST_UPDATE_STRING)




MENU = PageMenu()
MENU.add_entry('Home', 'index.html')
MENU.add_entry('Curriculum vit&aelig;', 'cv.html')
MENU.add_entry('Publications', 'publications.html')
MENU.add_entry('Presentations', 'talks.html')
MENU.add_entry('About me', 'aboutme.html')
MENU.add_entry('Links', 'links.html')
MENU.add_entry('Miscellanea', 'misc.html')
MENU.add_entry('Didattica', 'teaching.html')
MENU.add_entry('Private area', 'private')


def _indent(text: str, indent_level: int = 0) -> str:
    """Small utility function indent full paragraphs.

    This is essentially replacing any newline character prepending to it the
    proper number of spaces.

    Warning
    -------
    This is obsolete and should be removed, use helpers.HTML instead.
    """
    # Calculate the indentation.
    indent = INDENT_STRING * indent_level
    # Prepend the right number of spaces to each new line.
    text = text.replace('\n', '\n%s' % indent)
    # Prepend the right number of spaces to the paragraph itself.
    text = '%s%s' % (indent, text)
    return text


def footer_html() -> str:
    """Return the full html for the page footer.

    At this point in time the footer is the same for all pages and this is
    essentially returning the template (modulo the newline strip). In the
    future this might extended with additional, per-page, customization.
    """
    return FOOTER_TEMPLATE.strip('\n')


def _read_page_content(file_path: Optional[str] = None) -> str:
    """Retrieve the actual content for a given page.

    This is reading the local html file pointed by the function argument and
    returning its content verbatim.

    If the file path is None or the file does not exist, this is returning
    an empty string.
    """
    content = ''
    if file_path is None:
        return content
    if not os.path.exists(file_path):
        logging.warning('Could not find %s.', file_path)
        return content
    logging.info('Reading page content from %s...', file_path)
    with open(file_path, 'r') as input_file:
        content = input_file.read()
    return content


def page_html(title: str, menu_entry: Optional[str] = None,
              file_path: Optional[str] = None) -> str:
    """Return the full html for a generic web page, given all the relevant
    content.
    """
    # Indent all the elements properly.
    footer = _indent(footer_html(), 3)
    menu = _indent(MENU.to_html(menu_entry), 4)
    content = _read_page_content(file_path)
    # Horrible hack to add the publications. This should be handled properly
    # in a more general fashion (the menu should probably be aware of it.)
    if title == 'Publications':
        from webpage.orcid import ORCID
        orcid = ORCID()
        content = '{}{}'.format(content, orcid.publication_list_html())
    # End of hack.
    content = _indent(content, 5)
    # Fill in the template.
    return (PAGE_TEMPLATE % (title, menu, title, content, footer)).strip('\n')


def write_page(title: str, menu_entry: str, file_path: str):
    """Write a single html page to file.
    """
    logging.info('Processing page "%s"...', title)
    output_file_path = html_output_file_path(file_path)
    logging.info('Writing output file to %s...', output_file_path)
    text = page_html(title, menu_entry, file_path)
    with open(output_file_path, 'w') as output_file:
        output_file.write(text)
    logging.info('Done.')


def write_menu_pages():
    """Write all the html pages in the menu to file.
    """
    for title in MENU:
        if MENU.target_points_to_file(title):
            file_path = MENU.target_file_path(title, CONTENTS_FOLDER)
            write_page(title, title, file_path)


def write_about_page():
    """Write the "About this website" page.

    This needs a separate method, as it is not driven by the menu, nor linked
    therein.
    """
    title = 'About this website'
    target = content_file_path('about.html')
    write_page(title, None, target)


def _copy(src: str, dest: str):
    """Small utility functions to copy files.
    """
    logging.info('Copying %s -> %s...', src, dest)
    shutil.copyfile(src, dest)


def copy_style_sheets():
    """Copy the relevant style sheets from the local source folder to the
    output html folder to be copied on the remote server.
    """
    logging.info('Copying style sheets...')
    for css in STYLE_SHEETS:
        src = os.path.join(CSS_FOLDER, css)
        dest = os.path.join(CSS_OUTPUT_FOLDER, css)
        _copy(src, dest)


def copy_images(file_formats=('png',)):
    """Copy all the relevant images into the output folder.
    """
    logging.info('Copying images...')
    file_list = []
    for fmt in file_formats:
        file_list = glob.glob(os.path.join(IMG_FOLDER, '*.%s' % fmt))
    for src in file_list:
        dest = os.path.join(IMG_OUTPUT_FOLDER, os.path.basename(src))
        _copy(src, dest)


def deploy():
    """Deploy the glorious website.
    """
    create_local_tree()
    write_menu_pages()
    write_about_page()
    copy_style_sheets()
    copy_images()
