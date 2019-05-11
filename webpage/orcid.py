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

"""Simple ORCID interface.
"""

import logging
import os
import json

from typing import Optional, List

import requests


class ORCID:

    """Lightweight interface to the ORCID restful API.

    (As lightweight as an interface to ORCID can be---for the love of God, those
    guys really did go overboard adding layers and layers of information. It
    is clear that I am not understanding this at all. Anyways.)

    The basic idea for this came from
    http://kitchingroup.cheme.cmu.edu/blog/2015/03/28/The-orcid-api-and-generating-a-bibtex-file-from-it/
    which is now outdated---things do not quite work the same way they used to
    back in 2015.

    This seems to be a useful resource:
    https://members.orcid.org/api/tutorial/read-orcid-records

    Endpoint              : Description

    /record               : Summary view of the full ORCID record
    /person               : Biographical section of the ORCID record, including
                            through /researcher-urls below
    /address              : The researcher’s countries or regions
    /email                : The email address(es) associated with the record
    /external-identifiers : Linked external identifiers in other systems
    /keywords             : Keywords related to the researcher and their work
    /other-names          : Other names by which the researcher is known
    /personal-details     : Personal details: the researcher’s name, credit
                            (published) name, and biography
    /researcher-urls      : Links to the researcher’s personal or profile pages
    /activities           : Summary of the activities section of the ORCID
                            record, including through /works below.
    /educations           : Education affiliations
    /employments          : Employment affiliations
    /fundings             : Summary of funding activities
    /peer-reviews         : Summary of peer review activities
    /works                : Summary of research works

    Now, all the endpoint can apparently be used next to the basic url, i.e.,
    one can send a request to  http://pub.orcid.org/0000-0002-9785-7726/works'
    to dump all the works by the owner of the ORCID.

    Internally all the paths refer to the basic url http://pub.orcid.org/

    One interesting thing is that the each work seems to have a put-code
    key representing a unique handle that can then be used to retrieve the
    full information about the work itself, e.g.,
    http://pub.orcid.org/0000-0002-9785-7726/work/25306957
    This is also available as the path property in the work description.
    """

    BASE_URL = 'http://pub.orcid.org'
    LOCAL_FOLDER = os.path.abspath(os.path.join(os.path.basename(__file__),
                                                '..', 'orcid'))

    def __init__(self, orcid_id: str = '0000-0002-9785-7726',
                 force_fetch: bool = False) -> None:
        """Constructor.

        Here we are essentially fetching the ORCID data from either a local
        json file or the ORCID server.
        """
        self.orcid_id = orcid_id
        # Fetch the top-level ORCID data.
        self.data = self._load(self._url(), self._file_path(), force_fetch)
        # Loop over the works and fetch all the detailed work information.
        # Admittedly we could do a cleaner job, here---but it's only done once.
        self.work_list: List[dict] = []
        for work in self.data['activities-summary']['works']['group']:
            summary = work['work-summary'][0]
            path = summary['path']
            put_code = summary['put-code']
            url = self._url(path)
            file_name = '{}-work-{}.json'.format(self.orcid_id, put_code)
            file_path = self._file_path(file_name)
            # Mind we're never forcing re-fetching individual works from the
            # server, as they typically not changing.
            self.work_list.append(self._load(url, file_path, force_fetch=False))

    def _url(self, path: Optional[str] = None):
        """Simple utility to concatenate url elements to the base ORCID url.

        Mind all the path elements in the json dictionaries refer to the base
        url and have a leading /, so this method is consistent with that.
        """
        if path is None:
            path = '/{}'.format(self.orcid_id)
        return '{}{}'.format(self.BASE_URL, path)

    def _file_path(self, file_name: Optional[str] = None) -> str:
        """Return the full absolute path to the file with a given name in the
        local folder (can be used in either read or write mode).
        """
        if file_name is None:
            file_name = '{}.json'.format(self.orcid_id)
        return os.path.join(self.LOCAL_FOLDER, file_name)

    @classmethod
    def _fetch(cls, url: str, output_file_path: str) -> dict:
        """Generic fetch function to send a request to the server and save
        the response to a json file.

        Return the data fetched from the server.
        """
        logging.info('Fetching data from %s...', url)
        resp = requests.get(url, headers={'Accept':'application/orcid+json'})
        with open(output_file_path, 'w') as output_file:
            logging.info('Writing data to %s...', output_file_path)
            data = resp.json()
            json.dump(data, output_file)
        return data

    @classmethod
    def _read(cls, input_file_path: str) -> dict:
        """Read data from a local jsone file.
        """
        logging.debug('Reading data from %s...', input_file_path)
        with open(input_file_path) as input_file:
            data = json.load(input_file)
        return data

    @classmethod
    def _load(cls, url: str, file_path: str,
              force_fetch: bool = False) -> dict:
        """Load some ORCID data from either a local json file (if it exists
        and the force_fetch flag is set to False), or fetching directly from
        the server.

        Note that file_path points to either the input or the output file
        in the two cases.
        """
        if os.path.exists(file_path) and not force_fetch:
            return cls._read(file_path)
        return cls._fetch(url, file_path)

    @classmethod
    def _dump(cls, json_item: dict, sort_keys: bool = False) -> str:
        """Formatting function for json elements.
        """
        return json.dumps(json_item, sort_keys=sort_keys, indent=2,
                          separators=(',', ': '))

    @classmethod
    def _work_summary(cls, work: dict) -> dict:
        """Return the summary for a work element.

        The work summary is a dictionary with the following keys:
        - put-code
        - created-date
        - last-modified-date
        - source
        - title
        - external-ids
        - type
        - publication-date
        - visibility
        - path
        - display-index

        The path is what you want to use to retrieve the detailed record
        information.
        """
        return work['work-summary'][0]

    def publication_list(self):
        """Do something.
        """
        return

    def __str__(self) -> str:
        """String representation.
        """
        return self._dump(self.data)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    orcid = ORCID()
    orcid.publication_list()
    print(orcid.LOCAL_FOLDER)
    #url = 'http://pub.orcid.org/0000-0002-9785-7726/work/25306957'
    #url = 'http://pub.orcid.org/0000-0002-9785-7726/works'
    #resp = requests.get(url, headers={'Accept':'application/orcid+json'})
    #data = resp.json()
    #print(json.dumps(data))
