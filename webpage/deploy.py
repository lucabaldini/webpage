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

from webpage.website import deploy
from webpage.helpers import ArgumentParser


def main() -> None:
    """Deploy the webpage.

    Warning
    -------
    Consider moving this into the website module (and rename that as deploy).
    """
    parser = ArgumentParser()
    parser.add_argument('--upload', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    deploy(args.upload)



if __name__ == '__main__':
    main()
