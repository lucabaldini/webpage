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
import glob
import logging

import webpage
from webpage.core import PageMenu, HTML
from webpage.helpers import copy
from webpage.orcid import ORCID


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
STYLE_SHEETS = ['default.css']
DEFAULT_STYLE_SHEET = STYLE_SHEETS[0]
DEFAULT_CSS_HREF = '%s/%s' % (webpage.CSS_FOLDER_NAME, DEFAULT_STYLE_SHEET)


def page_template() -> str:
    """Create the basic template for all the HTML pages in the website.

    The function is reading the basic template in the html file in the contents
    folder and fillin-in all the runtime information that can be calculated
    once and forever at the beginning, such as the last update. The template can
    then be interpolated to add the menu and the actual content.

    Maybe this can be memoized?
    """
    text = webpage.read_content('template.html')
    text = text.format(base_title=PAGE_BASE_TITLE,
                       keywords=PAGE_KEYWORDS_STRING,
                       description=PAGE_DESCRIPTION, author=PAGE_AUTHOR,
                       css_target=DEFAULT_CSS_HREF, header=PAGE_HEADER_TEXT,
                       copyright_start=COPYRIGHT_START_YEAR,
                       copyright_end=COPYRIGHT_END_YEAR,
                       last_update=LAST_UPDATE_STRING)
    return text


MENU = PageMenu()
MENU.add_entry('Home', 'index.html')
MENU.add_entry('Curriculum vit&aelig;', 'cv.html')
MENU.add_entry('Publications', 'publications.html', ORCID().work_list_html)
MENU.add_entry('Presentations', 'talks.html')
MENU.add_entry('About me', 'aboutme.html')
MENU.add_entry('Links', 'links.html')
MENU.add_entry('Miscellanea', 'misc.html')
MENU.add_entry('Didattica', 'teaching.html')
MENU.add_entry('Private area', 'private')


def _write_page(title: str, target: str, hook=None) -> None:
    """Write a single html page to file.

    This is the main workhorse function to wirte static html web pages.
    """
    logging.info('Processing page "%s"...', title)
    template = page_template()
    menu = HTML.indent(MENU.html(title), 4)
    content = HTML.indent(webpage.read_content(target), 4)
    if hook is not None:
        content = '{}\n\n{}'.format(content, hook())
    text = template.format(title, menu, title, content)
    output_file_path = webpage.output_file_path(target)
    logging.info('Writing output file to %s...', output_file_path)
    with open(output_file_path, 'w') as output_file:
        output_file.write(text)
    logging.info('Done.')


def write_static_pages():
    """Write all the html pages in the menu to file.
    """
    # Write the static pages driven by the menu.
    for title, (target, hook) in MENU.items():
        if MENU.target_points_to_file(title):
            _write_page(title, target, hook)
    # And write everything else is necessary.
    _write_page('About this website', 'about.html')


def copy_style_sheets():
    """Copy the relevant style sheets from the local source folder to the
    output html folder to be copied on the remote server.
    """
    logging.info('Copying style sheets...')
    for css in STYLE_SHEETS:
        src = os.path.join(webpage.CSS_FOLDER, css)
        dest = os.path.join(webpage.OUTPUT_CSS_FOLDER, css)
        copy(src, dest)


def copy_images(file_formats=('png',)):
    """Copy all the relevant images into the output folder.
    """
    logging.info('Copying images...')
    file_list = []
    for fmt in file_formats:
        file_list = glob.glob(os.path.join(webpage.IMG_FOLDER, '*.%s' % fmt))
    for src in file_list:
        dest = os.path.join(webpage.OUTPUT_IMG_FOLDER, os.path.basename(src))
        copy(src, dest)


def deploy():
    """Deploy the glorious website.
    """
    webpage.create_local_tree()
    write_static_pages()
    copy_style_sheets()
    copy_images()
