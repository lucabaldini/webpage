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


import datetime
import os
import sys
import shutil
import glob
import logging

from typing import Optional


"""Basic configuration.
"""
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


"""Basic remote environment.
"""
REMOTE_CSS_FOLDER = 'css'
REMOTE_IMG_FOLDER = 'images'
DEFAULT_CSS_HREF = '%s/%s' % (REMOTE_CSS_FOLDER, DEFAULT_STYLE_SHEET)


"""Basic local environment.
"""
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
            logging.info('Creating output folder %s...' % folder)
            os.mkdir(folder)


"""The basic template for all the web pages in the site.
"""
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


"""Template for the page footer.
"""
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


"""Basic structure of the menu for the website.

This is essentially a tuple of (title, targte) tuples, which is used to 
control the menu and to pupulate the actual html of the pages themselves.

Note that the target is intented in the html space, and can be either 
a file name or a folder name.

The mechanism relies on the fact that the dictionary are now preserving the
insertion order in Python.
"""
MENU_DICT = {
    'Home': 'index.html',
    'Curriculum vit&aelig;': 'cv.html',
    'Publications': 'publications.html',
    'Presentations': 'talks.html',
    'About me': 'aboutme.html',
    'Links': 'links.html',
    'Miscellanea': 'misc.html',
    'Didattica': 'teaching.html',
    'Private area': 'private'
}


def menu_target(title: str) -> str:
    """Return the menu target associated with a given title.
    """
    return MENU_DICT[title]


def menu_has_target_file(title: str) -> bool:
    """Return true if an actual html file is associated with a page title in
    the menu.
    """
    return menu_target(title).endswith('.html')
    

def menu_file_name(title: str) -> Optional[str]:
    """Return the name of the html target file for a given page title.

    If the target is not a html file name (i.e., does not end with ".html")
    the function is returning None.
    """
    if menu_has_target_file(title):
        return menu_target(title)


def _menu_file_path(title: str, folder: str) -> Optional[str]:
    """Small convenience function to joint a menu target file name with a
    generic folder path.
    """
    file_name = menu_file_name(title)
    if file_name is not None:
        return os.path.join(folder, file_name)


def content_file_path(title: str) -> Optional[str]:
    """Return the full absolulte path to the (local) file containing the
    actual content for the page with a given title.

    This assumes that names of the local files map one to one into the 
    file names for the actual web pages.
    """
    return _menu_file_path(title, CONTENTS_FOLDER)


def output_file_path(title: str) -> Optional[str]:
    """Return the full ansolute path to the output html file, i.e., the local
    file that eventually needs to be copied over to the remote server.
    """
    return _menu_file_path(title, HTML_OUTPUT_FOLDER)


def _indent(text: str, indent_level: int=0) -> str:
    """Small utility function indent full paragraphs.

    This is essentially replacing any newline character prepending to it the
    proper number of spaces.
    """
    # Calculate the indentation.
    indent = INDENT_STRING * indent_level
    # Prepend the right number of spaces to each new line.
    text = text.replace('\n', '\n%s' % indent)
    # Prepend the right number of spaces to the paragraph itself.
    text = '%s%s' % (indent, text)
    return text


def menu_html(current_title: str) -> str:
    """Return the full html for the page menu.
    """
    menu = '<ul>\n'
    for title, target in MENU_DICT.items():
        if title == current_title:
            menu += '%s<li class=current>%s</li>\n' % (INDENT_STRING, title)
        else:
            menu += '%s<li><a href=%s>%s</a></li>\n' %\
                    (INDENT_STRING, target, title)
    menu = '%s</ul>' % menu
    return menu
    

def footer_html() -> str:
    """Return the full html for the page footer.
    """
    return FOOTER_TEMPLATE.strip('\n')


def page_content_html(title: str) -> str:
    """Retrieve the actual content for a given page.
    """
    file_path = content_file_path(title)
    content = ''
    if file_path is None:
        return content
    if not os.path.exists(file_path):
        logging.warning('Could not find %s.' % file_path)
        return content
    logging.info('Reading page content from %s...' % file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    return content


def page_html(title: str) -> str: 
    """Return the full html for a generic web page, given all the relevant
    content.
    """
    # Indent all the elements properly.
    footer = _indent(footer_html(), 3)
    menu = _indent(menu_html(title), 4)
    content = _indent(page_content_html(title), 5)
    # Fill in the template.
    return (PAGE_TEMPLATE % (title, menu, title, content, footer)).strip('\n')


def write_page(title: str):
    """Write a single html page to file.
    """
    logging.info('Processing page "%s"...' % title)
    file_path = output_file_path(title)
    logging.info('Writing output file to %s...' % file_path)
    text = page_html(title)
    with open(file_path, 'w') as f:
        f.write(text)
    logging.info('Done.')


def write_menu_pages():
    """Write all the html pages in the menu to file.
    """
    logging.info('Writing all menu pages...')
    for title, target in MENU_DICT.items():
        if menu_has_target_file(title):
            write_page(title)


def _copy(src: str, dest: str):
    """Small utility functions to copy files.
    """
    logging.info('Copying %s -> %s...' % (src, dest))
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


def copy_images(file_formats=['png']):
    """Copy all the relevant images into the output folder.
    """
    logging.info('Copying images...')
    file_list = []
    for fmt in file_formats:
        file_list = glob.glob(os.path.join(IMG_FOLDER, '*.%s' % fmt))
    for src in file_list:
        dest = os.path.join(IMG_OUTPUT_FOLDER, os.path.basename(src))
        _copy(src, dest)


def deploy(logging_level=logging.DEBUG):
    """Deploy the glorious website.
    """
    logging.basicConfig(level=logging_level)
    create_local_tree()
    write_menu_pages()
    copy_style_sheets()
    copy_images()



if __name__ == '__main__':
    deploy()
