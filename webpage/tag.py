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


"""Rudimentary release manager.
"""

import os
import sys
import logging
import datetime
import textwrap

from webpage import WEBPAGE_FOLDER, RELEASE_NOTES
from webpage.helpers import cmd, cmdoutput, ArgumentParser
from webpage.version import version as current_version


TAG_MODES = ['major', 'minor', 'patch']


def bump_version(mode: str) -> str:
    """Bump the version (either the major, minor or patch bit).
    """
    logging.info('Bumping version %s (%s)...', current_version, mode)
    assert mode in TAG_MODES
    major, minor, patch = (int(item) for item in current_version.split('.'))
    if mode == 'major':
        major += 1
        minor = 0
        patch = 0
    elif mode == 'minor':
        minor += 1
        patch = 0
    elif mode == 'patch':
        patch += 1
    new_version = '{}.{}.{}'.format(major, minor, patch)
    logging.info('New version is %s', new_version)
    return new_version


def update_version_file(version: str, timestamp: str, revision: str) -> None:
    """Update the version file.
    """
    file_path = os.path.join(WEBPAGE_FOLDER, 'version.py')
    logging.info('Writing version file "%s"...', file_path)
    text = """\
    # Automatically created by {}, do not edit by hand.
    # pylint: skip-file
    #
    version = "{}"
    release_date = "{}"
    revision = "{}"
    """.format(__file__, version, timestamp, revision)
    text = textwrap.dedent(text)
    with open(file_path, 'w') as input_file:
        input_file.write(text)
    logging.info('Done.')


def update_release_notes(version: str, timestamp: str, revision: str) -> None:
    """Update the release notes.

    This prepends a line to the release notes with the tag information.
    """
    lines = []
    # Read the current version of the relase notes.
    with open(RELEASE_NOTES, 'r') as input_file:
        # Read the first line and make sure it's right.
        line = input_file.readline()
        assert line == 'Release notes\n'
        lines.append(line)
        # Read the second line and make sure it's right.
        line = input_file.readline()
        assert line == '=============\n'
        lines.append(line)
        # Append the release-manager-generated line.
        line = '\n\n*webpage {} ({}) - {}*\n'.format(version, revision, timestamp)
        lines.append(line)
        # Skip any leading empty line.
        line = ' '
        while line.isspace():
            line = input_file.readline()
        # Add the remaining lines (mind the last from the last step is relevant.)
        lines.append(line)
        lines += input_file.readlines()
    print(''.join(lines))
    # Write all the crap to file.
    logging.info('Updating release notes...')
    with open(RELEASE_NOTES, 'w') as output_file:
        output_file.writelines(lines)
    logging.info('Done.')


def tag(version: str) -> None:
    """Tag a new version of the package.
    """
    git_branch = cmdoutput('git', 'rev-parse', '--abbrev-ref', 'HEAD')
    if git_branch != 'master':
        sys.exit('Trying to tag a branch different from the master... Abort.')
    cmd('git', 'pull')
    cmd('git', 'status')
    timestamp = str(datetime.datetime.now())
    revision = cmdoutput('git', 'rev-parse', 'HEAD')
    update_version_file(version, timestamp, revision)
    update_release_notes(version, timestamp, revision)
    msg = 'Prepare for tag %s.' % version
    cmd('git', 'commit', '-a', '-m "{}"'.format(msg))
    cmd('git', 'push')
    msg = 'Tagging version {}'.format(version)
    cmd('git', 'tag', '-a', '{}'.format(version), '-m "{}"'.format(msg))
    cmd('git', 'push', '--tags')


def release() -> None:
    """Release a new version of the webpage.
    """
    parser = ArgumentParser()
    parser.add_argument('--tagmode', required=True, choices=TAG_MODES)
    args = parser.parse_args()
    version = bump_version(args.tagmode)
    tag(version)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    release()
