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

import logging
import os
import shutil
import functools


def mktree(folder_path: str) -> None:
    """Create a directory tree, if it does not exist already.
    """
    if not os.path.exists(folder_path):
        logging.info('Creating folder %s...', folder_path)
        os.mkdir(folder_path)


def copy(src: str, dest: str) -> None:
    """Small utility functions to copy files.
    """
    logging.info('Copying %s -> %s...', src, dest)
    shutil.copyfile(src, dest)


def memoize(func):
    """Simple decorator to memoize the return value of a function with no
    argument.

    See https://stackoverflow.com/questions/5630409
    for the use of nonlocal in the body of the wrapper function.
    """
    @functools.wraps(func)
    cache = None
    def wrapper():
        nonlocal cache
        if cache is None:
            cache = func()
        return cache
    return wrapper
