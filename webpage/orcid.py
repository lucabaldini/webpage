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
import datetime

from typing import Optional, List, Any

import requests

from webpage import ORCID_FOLDER
from webpage.core import HTML, LaTeX


class Work(dict):

    """Class describing a work in the ORCID sense.

    The top-level keys from the json object that the request to the ORCID
    server (with a /work/* path) retrns is:
    - created-date
    - last-modified-date
    - source
    - put-code
    - path
    - title
    - journal-title
    - short-description
    - citation
    - type
    - publication-date
    - external-ids
    - url
    - contributors
    - language-code
    - country
    - visibility

    Most of these keys actually map to nested dicts, so the parsing of the
    object is non trivial.
    """

    def __init__(self, work_dict: dict) -> None:
        """Constructor.
        """
        super().__init__(self)
        self.update(work_dict)
        # We perform the following two raw (unguarded) accesses to the dict content
        # as a minimal diagnostics tool in case something goes wrong. All the
        # rest should be embedded into a _navigate() call.
        self.path = self['path']
        self.title = self['title']['title']['value']
        # And the following is the minimum info refer to the paper to in case
        # we want to print out some diagnostics.
        self.info = 'path {} ({})'.format(self.path, self.title)
        self.date = self.__date()
        self.external_ids = self.__external_ids()
        self.author_string = self.__author_string()

    def _navigate(self, *keys, default: Any = None, quiet: bool = False):
        """Helper function to access nested values in the top-level dictionary.

        Given a list of keys, this method is navigating the dictionary down all
        the necessary levels. At each level the dictionary access is wrapped
        into a try/except block so that if something goes wrong we do have full
        information about what has gone wrong.
        """
        item = self
        for key in keys:
            try:
                item = item[key]
            except TypeError as exception:
                if quiet:
                    return default
                msg = 'Cannot navigate %s for %s. ' +\
                      'Offending key is \'%s\', with underlying exception: %s.'
                logging.warning(msg, keys, self.info, key, exception)
                return default
        return item

    def __date(self) -> datetime.date:
        """Return the publication date.

        This is another one that we implement in the form of a private
        frunction to avoid re-calculating things multiple times (and we need
        the date to sort records anyway).

        One major issue that we are having here is that month and day seem to
        be almost never defined in the record, and therefore sortin within the
        same year is essentially impossible. This is the reason why we are
        calling the corresponding _navigate() bits in quiet mode, and with an
        explicit default value.
        """
        year = self._navigate('publication-date', 'year', 'value')
        month = self._navigate('publication-date', 'month', 'value', quiet=True, default=1)
        day = self._navigate('publication-date', 'day', 'value', quiet=True, default=1)
        return datetime.date(int(year), int(month), int(day))

    def __external_ids(self) -> dict:
        """Return a dictionary with all the external identifiers.

        Note we implement this as a "private" class method that is called only
        once in the constructor and cache the external ids so that we do not
        recalculate them multiple times .
        """
        ids = {}
        for item in self._navigate('external-ids', 'external-id'):
            ids[item['external-id-type']] = item['external-id-value']
        return ids

    @staticmethod
    def _format_credit_name(contributor: dict) -> str:
        """Formatting facility for the author names.

        At this point this is a no-op, but we might use some intelligence, here,
        to format the names in a uniform fashion.
        """
        name = contributor['credit-name']['value']
        return name

    def __author_string(self, max_num_authors: int = 8) -> str:
        """Return a formatted author list.

        The author list is truncated to the maximum number of authors, and, if
        necessary, complemented with "et al." and the total number of authors
        in parenthesis.
        """
        contributors = self._navigate('contributors', 'contributor')
        try:
            num_authors = len(contributors)
        except TypeError as exception:
            logging.warning(exception)
            num_authors = 0
        if num_authors == 0:
            msg = 'Empty author list for %s'
            logging.warning(msg, self.info)
            return ''
        contributors = contributors[:max_num_authors]
        names = (self._format_credit_name(item) for item in contributors)
        author_string = ', '.join(names)
        if num_authors > max_num_authors:
            author_string = '{} et al.'.format(author_string)
        return author_string

    def type_(self) -> str:
        """Return the type of the work.
        """
        return self._navigate('type')

    def journal(self) -> str:
        """Return the journal name for the work.
        """
        return self._navigate('journal-title', 'value')

    def year(self) -> Optional[int]:
        """Return the year of the publication.
        """
        return self.date.year

    def doi(self) -> str:
        """Return the doi of the publication.
        """
        return self.external_ids.get('doi', None)

    def doi_url(self) -> str:
        """Return the DOI url corresponding to the publication.
        """
        doi = self.doi()
        if doi is None:
            return None
        return 'https://doi.org/{}'.format(doi)

    def ascii(self) -> str:
        """ASCII representation.
        """
        return '{}, "{}", {} ({})'.format(self.author_string, self.title,
                                          self.journal(), self.year())

    def html(self) -> str:
        """HTML formatting.
        """
        title = HTML.emph(HTML.hyperlink(self.title, self.doi_url()))
        journal = self.journal()
        if journal is None:
            return '{}, "{}" ({})'.format(self.author_string, title, self.year())
        else:
            return '{}, "{}", {} ({})'.format(self.author_string, title,
                                              journal, self.year())

    def latex(self) -> str:
        """LaTeX formatting.
        """
        title = LaTeX.hyperlink(LaTeX.emph(self.title), self.doi_url())
        journal = self.journal()
        if journal is None:
            return '{}, "{}" ({})'.format(self.author_string, title, self.year())
        else:
            return '{}, "{}", {} ({})'.format(self.author_string, title,
                                              journal, self.year())

    def __lt__(self, other) -> bool:
        """Comparison operator so sort publication lists.
        """
        return self.date < other.date

    def __str__(self) -> str:
        """String representation.
        """
        return self.ascii()



class WorkList(List[Work]):

    """Class representing a list of ORCID works.

    And, in human language, this is really a publication list.
    """

    def _format(self, year_formatter, work_formatter):
        """
        """
        lines = []
        current_year = None
        for i, work in enumerate(self):
            if work.year() != current_year:
                # Drop a special entry for the year in case of change.
                lines.append('{}'.format(year_formatter(work.year())))
                current_year = work.year()
            # And this is the actual element for the publication.
            lines.append('[{}] {}'.format(i + 1, work_formatter(work)))
        return lines

    def ascii(self) -> str:
        """ASCII representation.
        """
        lines = self._format(str, Work.ascii)
        return '\n'.join(lines)

    def html_simple(self, indent: int = 4) -> str:
        """HTML representation.

        Legacy function returning the simplest possible HTML representation
        (i.e., a simple unordered list with no class specifications).
        """
        lines = self._format(HTML.heading3, Work.html)
        return HTML.list(lines, indent)

    def  html(self, indent: int = 4) -> str:
        """HTML representation.

        We initially though we could do this reusing the logic in the _format()
        class method, but that made unnecessarily convolute specifying
        different li HTML attributes for lines representing years and those
        representing actual publications, so we're resorting to an explicit
        loop, here.
        """
        lines = [HTML.tag_open('ul', indent, class_='publication-list')]
        current_year = None
        for i, work in enumerate(self):
            if work.year() != current_year:
                class_ = 'publication-year'
                lines.append(HTML.list_item(str(work.year()), indent + 1, class_))
                current_year = work.year()
            class_ = 'publication-item'
            text = '[{}] {}'.format(i + 1, work.html())
            lines.append(HTML.list_item(text, indent + 1, class_))
        lines.append(HTML.tag_close('ul', indent))
        return '\n'.join(lines)

    def latex(self) -> str:
        """LaTeX representation.

        Warning
        -------
        This is untested.
        """
        lines = self._format(str, Work.latex)
        return '\n'.join(lines)

    def __str__(self) -> str:
        """Text representation.
        """
        return self.ascii()




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

    =====================  =====================================================
    Endpoint               Description
    =====================  =====================================================
    /record                Summary view of the full ORCID record
    /person                Biographical section of the ORCID record, including
                           through /researcher-urls below
    /address               The researcher’s countries or regions
    /email                 The email address(es) associated with the record
    /external-identifiers  Linked external identifiers in other systems
    /keywords              Keywords related to the researcher and their work
    /other-names           Other names by which the researcher is known
    /personal-details      Personal details: the researcher’s name, credit
                           (published) name, and biography
    /researcher-urls       Links to the researcher’s personal or profile pages
    /activities            Summary of the activities section of the ORCID
                           record, including through /works below.
    /educations            Education affiliations
    /employments           Employment affiliations
    /fundings              Summary of funding activities
    /peer-reviews          Summary of peer review activities
    /works                 Summary of research works
    =====================  =====================================================

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
    LOCAL_FOLDER = ORCID_FOLDER

    def __init__(self, orcid_id: str = '0000-0002-9785-7726', force_fetch: bool = False) -> None:
        """Constructor.

        Here we are essentially fetching the ORCID data from either a local
        json file or the ORCID server.
        """
        self.orcid_id = orcid_id
        # Fetch the top-level ORCID data.
        self.data = self._load(self._url(), self._file_path(), force_fetch)
        # Loop over the works and fetch all the detailed work information.
        # Admittedly we could do a cleaner job, here---but it's only done once.
        self.work_list = WorkList()
        logging.info('Populating work list...')
        for work in self.data['activities-summary']['works']['group']:
            summary = self.work_summary(work)
            path = summary['path']
            put_code = summary['put-code']
            url = self._url(path)
            file_name = '{}-work-{}.json'.format(self.orcid_id, put_code)
            file_path = self._file_path(file_name)
            # Mind we're never forcing re-fetching individual works from the
            # server, as they typically not changing.
            work = Work(self._load(url, file_path, force_fetch=False))
            self.work_list.append(work)
        logging.info('Sorting work list...')
        self.work_list.sort(reverse=True)

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

    @staticmethod
    def _fetch(url: str, output_file_path: str) -> dict:
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

    @staticmethod
    def _read(input_file_path: str) -> dict:
        """Read data from a local jsone file.
        """
        logging.debug('Reading data from %s...', input_file_path)
        with open(input_file_path) as input_file:
            data = json.load(input_file)
        return data

    @classmethod
    def _load(cls, url: str, file_path: str, force_fetch: bool = False) -> dict:
        """Load some ORCID data from either a local json file (if it exists
        and the force_fetch flag is set to False), or fetching directly from
        the server.

        Note that file_path points to either the input or the output file
        in the two cases.
        """
        if os.path.exists(file_path) and not force_fetch:
            return cls._read(file_path)
        return cls._fetch(url, file_path)

    @staticmethod
    def dump(json_item: dict, sort_keys: bool = False) -> str:
        """Formatting function for json elements.
        """
        return json.dumps(json_item, sort_keys=sort_keys, indent=2, separators=(',', ': '))

    @staticmethod
    def work_summary(work: dict) -> dict:
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

    def __str__(self) -> str:
        """String representation.
        """
        return self.dump(self.data)
