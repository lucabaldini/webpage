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

import requests
import json
import logging
import os


class ORCID:

    """Lightweight interface to the ORCID restful API.

    http://kitchingroup.cheme.cmu.edu/blog/2015/03/28/The-orcid-api-and-generating-a-bibtex-file-from-it/
    https://members.orcid.org/api/tutorial/reading-xml
    """

    BASE_URL = 'http://pub.orcid.org/'
    DATA_FILE_PATH = 'orcid_data.json'

    def __init__(self, force_fetch=False):
        """Constructor.
        """
        if not os.path.exists or force_fetch is True:
            self.data = self._fetch_data()
        else:
            self.data = self._read_data()
            
    def _fetch_data(self, orcid_id: str = '0000-0002-9785-7726') -> dict:
        """Fetch the ORCID data for the selected ORCID identifier and save them
        to the local .json file.

        Note this is returning the ORCID data in the form of gigantic
        dictionary, so they are immediately available to be consumed. 
        """
        url = '{}{}'.format(self.BASE_URL, orcid_id)
        resp = requests.get(url, headers={'Accept':'application/orcid+json'})
        with open(self.DATA_FILE_PATH, 'w') as output_file:
            logging.info('Downloading ORCID data to %s...', self.DATA_FILE_PATH)
            data = resp.json()
            json.dump(data, output_file)
        return data

    def _read_data(self) -> dict:
        """Read the ORCID data from the local .json file.
        """
        with open(self.DATA_FILE_PATH) as input_file:
            logging.info('Reading ORCID data from %s...', self.DATA_FILE_PATH)
            data = json.load(input_file)
        return data

    def publication_list(self):
        """https://members.orcid.org/api/tutorial/reading-xml
        """
        #print(self.data['activities-summary'].keys())
        a = self.data['activities-summary']['works']['group']
        for i, item in enumerate(a):
            print(json.dumps(item, sort_keys=True, indent=4, separators=(',', ': ')))         
            #b = item['work-summary'][0]
            #print(json.dumps(b, sort_keys=True, indent=4, separators=(',', ': ')))
            
            #print(b['type'])
            #if b['type'] == 'OTHER':
            #    print(b)
            input()
        #    print(i, b.keys(), b['title'], '\n')
        #for i, result in enumerate(self.data['orcid-profile']['orcid-activities']['orcid-works']['orcid-work']):
        #    print(i)
        #    print(result['work-citation']['citation'].encode('utf-8') + '\n')



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    orcid = ORCID()
    orcid.publication_list()
    #print(json.dumps(resp.json(), sort_keys=True, indent=4, separators=(',', ': ')))
