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


import os
import logging

from webpage.helpers import mktree


# Basic local environment.
#
BASE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def _webpage_folder(*args) -> str:
    """Path concatenation relatove to the bas package folder.
    (Avoids some typing.)
    """
    return os.path.join(BASE_FOLDER, *args)


# Input folders.
CONTENTS_FOLDER = _webpage_folder('contents')
CSS_FOLDER_NAME = 'css'
CSS_FOLDER = _webpage_folder(BASE_FOLDER, CSS_FOLDER_NAME)
DOCS_FOLDER = _webpage_folder(BASE_FOLDER, 'docs')
IMG_FOLDER_NAME = 'images'
IMG_FOLDER = _webpage_folder(BASE_FOLDER, IMG_FOLDER_NAME)
ORCID_FOLDER = _webpage_folder(BASE_FOLDER, 'orcid')


def content_file_path(file_name: str) -> str:
    """Return the path to a content file path.
    """
    return os.path.join(CONTENTS_FOLDER, file_name)


def read_content(file_name: str) -> str:
    """Retrieve the actual content for a given page.

    This is reading the local html file pointed by the function argument and
    returning its content verbatim. Mind we're passing the file by name and not
    by the full path. The file is assumed to live in the CONTENTS_FOLDER.
    """
    content = ''
    file_path = content_file_path(file_name)
    if not os.path.exists(file_path):
        logging.warning('Could not find {}.'.format(file_path))
        return content
    logging.info('Reading page content from {}...'.format(file_path))
    with open(file_path, 'r') as input_file:
        content = input_file.read()
    return content


# Output folders
OUTPUT_FOLDER = _webpage_folder(BASE_FOLDER, 'html')
OUTPUT_CSS_FOLDER = _webpage_folder(OUTPUT_FOLDER, CSS_FOLDER_NAME)
OUTPUT_IMG_FOLDER = _webpage_folder(OUTPUT_FOLDER, IMG_FOLDER_NAME)


def create_local_tree() -> None:
    """Create the necessary local tree for the html output, if necessary.
    """
    for folder in [OUTPUT_FOLDER, OUTPUT_CSS_FOLDER, OUTPUT_IMG_FOLDER]:
        mktree(folder)


def output_file_path(*args) -> str:
    """
    """
    return os.path.join(OUTPUT_FOLDER, *args)
