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


"""Deploy script for the webpage.
"""


import logging
logging.basicConfig(level=logging.INFO)


def _deploy(upload: bool = False) -> None:
    """
    """
    from webpage.website import deploy
    deploy(upload)



if __name__ == '__main__':
    from webpage.helpers import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--upload', action='store_true')
    args = parser.parse_args()
    _deploy(args.upload)
