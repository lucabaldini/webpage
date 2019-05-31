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
import sys
import logging
import datetime

from webpage import WEBPAGE_FOLDER
from webpage.helpers import cmd, cmdoutput
from webpage.version import version as current_version


TAG_MODES = ['major', 'minor', 'patch']


def bump_version(mode: str) -> str:
    """Bump the version (either the major, minor or patch bit).
    """
    logging.info('Bumping version {} ({})...'.format(current_version, mode))
    assert mode in TAG_MODES
    major, minor, patch = (int(item) for item in current_version.split('.'))
    if mode == 'major':
        major += 1
        release = 0
        patch = 0
    elif mode == 'minor':
        minor += 1
        patch = 0
    elif mode == 'patch':
        patch += 1
    new_version = '{}.{}.{}'.format(major, minor, patch)
    logging.info('New version is {}'.format(new_version))
    return new_version


def tag(version: str) -> None:
    """Tag a new version of the package.
    """
    git_branch = cmdoutput('git', 'rev-parse', '--abbrev-ref', 'HEAD')
    if git_branch != 'master':
        sys.exit('Trying to tag a branch different from the master... Abort.')
    cmd('git', 'pull')
    cmd('git', 'status')
    msg = 'Prepare for tag %s.' % version
    cmd('git', 'commit', '-a', '-m "{}"'.format(msg))
    cmd('git', 'push')
    msg = 'Tagging version {}'.format(version)
    cmd('git', 'tag', '-a {}'.format(version), '-m "{}"'.format(msg))
    cmd('git', 'push', '--tags')
    git_revision = cmdoutput('git', 'rev-parse', 'HEAD')
    return git_revision


def update_version_file(version: str, git_revision: str) -> None:
    """Update the version file.
    """
    file_path = os.path.join(WEBPAGE_FOLDER, 'version.py')
    logging.info('Writing version file "{}"...'.format(file_path))
    with open(file_path, 'w') as input_file:
        input_file.write('# Automatically created by {}.\n'.format(__file__))
        input_file.write('# Do not edit by hand.\n\n')
        input_file.write('version = "{}"\n'.format(version))
        input_file.write('release_date = "{}"\n'.format(datetime.datetime.now()))
        input_file.write('git_revision = "{}"\n'.format(git_revision))
    logging.info('Done.')


def release(mode: str) -> None:
    """Release a new version of the webpage.
    """
    version = bump_version(mode)
    git_revision = tag(version)
    update_version_file(version, git_revision)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    release('patch')
