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
import argparse
import subprocess


def cmd(*args: str) -> int:
    """Execute a command (small wrapper around subprocess.run()).
    """
    logging.info('About to execute command "%s"', (' '.join(args)))
    proc = subprocess.run(args)
    status = proc.returncode
    logging.info('Command completed with return code %s.', status)
    return status


def cmdoutput(*args: str, strip_endline: bool = True) -> str:
    """Small snipped to capture the command output.

    See https://stackoverflow.com/questions/4760215/ and
    https://stackoverflow.com/questions/606191
    """
    output = subprocess.run(args, stdout=subprocess.PIPE).stdout.decode('utf-8')
    if strip_endline:
        output = output.strip('\n')
    return output


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
    cache = None
    @functools.wraps(func)
    def wrapper():
        """Simple wrapper for the function call.
        """
        nonlocal cache
        if cache is None:
            cache = func()
        return cache
    return wrapper



class ArgumentFormatter(argparse.RawDescriptionHelpFormatter,
                        argparse.ArgumentDefaultsHelpFormatter):

    """Do nothing class combining our favorite formatting for the
    command-line options, i.e., the newlines in the descriptions are
    preserved and, at the same time, the argument defaults are printed
    out when the --help options is passed.

    The inspiration for this is coming from one of the comments in
    https://stackoverflow.com/questions/3853722
    """
    pass



class ArgumentParser(argparse.ArgumentParser):

    """Thin wrapper over argparse.ArgumentParser(), meant to standardize the
    command-line options for the gpdsw Python scripts.
    """

    def __init__(self, description=None, epilog=None):
        """Constructor.
        """
        formatter = ArgumentFormatter
        argparse.ArgumentParser.__init__(self, description=description,
                                         epilog=epilog,
                                         formatter_class=formatter)
