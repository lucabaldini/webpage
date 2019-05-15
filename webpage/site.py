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

"""Module containing all the facilities for the static html generation.
"""

import datetime
import os
import glob
import logging

import webpage
from webpage.core import PageMenu, HTML, ConferenceList
from webpage.helpers import copy
from webpage.orcid import ORCID


# Basic configuration.
#
PAGE_AUTHOR = 'Luca Baldini'
PAGE_DESCRIPTION = '%s\'s home page' % PAGE_AUTHOR
PAGE_BASE_TITLE = 'Luca Baldini @ UNIPI/INFN&ndash;Pisa'
PAGE_HEADER_TEXT = PAGE_BASE_TITLE
PAGE_KEYWORDS = ('Luca Baldini',
                 'INFN',
                 'University',
                 'Pisa',
                 'Physics',
                 'Astrophysics',
                 'Fermi',
                 'GLAST',
                 'IXPE')
PAGE_KEYWORDS_STRING = ', '.join(PAGE_KEYWORDS)
DATETIME_FORMAT = '%A, %B %d %Y at %H:%M'
LAST_UPDATE = datetime.datetime.now()
LAST_UPDATE_STRING = LAST_UPDATE.strftime(DATETIME_FORMAT)
COPYRIGHT_START_YEAR = 2012
COPYRIGHT_END_YEAR = LAST_UPDATE.year
STYLE_SHEETS = ['default.css']
DEFAULT_STYLE_SHEET = STYLE_SHEETS[0]
DEFAULT_CSS_HREF = '%s/%s' % (webpage.CSS_FOLDER_NAME, DEFAULT_STYLE_SHEET)

# Conferences.
#
CONFERENCE_LIST = ConferenceList()
"""
CONFERENCE_LIST.add_conference(
    '',
    '',
    '',
    '', ''
).add_contribution(
    ''
)
"""
CONFERENCE_LIST.add_conference(
    'CIV Congresso Nazionale della Società Italiana di Fisica',
    'Arcavacata di Rende (Italy)',
    'https://www.sif.it/attivita/congresso/104',
    '2018-09-17', '2018-09-21'
).add_contribution(
    'La missione Imaging X-ray Polarimetry Explorer (IXPE)', invited=True
)
CONFERENCE_LIST.add_conference(
    'Looking at Cosmic Sources in Polarized Light',
    'Osservatorio Astronomico di Asiago (Italy)',
    'http://www.pd.infn.it/astro/pers/asiago2018/',
    '2018-06-18', '2018-06-26'
).add_contribution(
    'X-ray Polarimetry: Simulation and Data Analysis',
    notes='series of invited lectures'
)
CONFERENCE_LIST.add_conference(
    'European Week of Astronomy and Space Science',
    'Liverpool (United Kingdom)',
    'https://eas.unige.ch/EWASS2018/',
    '2018-04-03', '2018-04-06'
).add_contribution(
    'The Imaging X-ray Polarimetry Explorer (IXPE) Mission ', invited=True
)
CONFERENCE_LIST.add_conference(
    'INFN in space: review of existing and forthcoming projects',
    'Laboratori Nazionali del Gran Sasso (Italy)',
    'https://agenda.infn.it/conferenceDisplay.py?confId=11788',
    '2016-07-20'
).add_contribution(
    'Prospettive per XIPE', invited=True
)
CONFERENCE_LIST.add_conference(
    'First XIPE Science Meeting',
    'Valencia (Spain)',
    'http://www.isdc.unige.ch/xipe/first-xipe-science-meeting.html',
    '2016-05-23', '2016-05-26'
).add_contribution(
    'ximpol: an X-ray polarimetry observation-simulation and analysis framework'
)
CONFERENCE_LIST.add_conference(
    'Sixth International Fermi Symposium',
    'Washington D.C. (USA)',
    'http://fermi.gsfc.nasa.gov/science/mtgs/symposia/2015/',
    '2015-11-09', '2015-11-13'
).add_contribution(
    'Pass 8 vs. Pass 7: How Statistically (In)Dependent Are They? (And Why Should You Care?)',
    poster=True
)
CONFERENCE_LIST.add_conference(
    'C Congresso Nazionale della Società Italiana di Fisica',
    'Pisa (Italy)',
    'http://www.sif.it/attivita/congresso/100',
    '2014-09-22', '2014-09-26'
).add_contribution(
    'Fermi Large Area Telescope science highlights', invited=True
)
CONFERENCE_LIST.add_conference(
    'ISAPP School 2014: Multi-wavelength and multi-messenger investigation of the visible and dark Universe',
    'Belgirate (Italy)',
    'http://isapp.school.2014.to.infn.it',
    '2014-07-21', '2014-07-30'
).add_contribution(
    'Review of cosmic-ray and gamma-ray space-based detectors',
    notes = 'series of invited lectures'
)
CONFERENCE_LIST.add_conference(
    'Astroparticle Physics 2014',
    'Amsterdam (The Netherlands)',
    'http://indico.cern.ch/conferenceDisplay.py?confId=278032',
    '2014-06-23', '2014-06-28'
).add_contribution(
    'The Fermi Large Area Telescope: status and prospects', invited=True
)

"""
add('High-energy cosmic-ray and gamma-ray detectors: experimental overview',
    'Mini-workshop sulla fisica astroparticellare al TeV e oltre',
    'Pisa (Italy)', '08/05/2014', '09/05/2014',
    'https://agenda.infn.it/conferenceDisplay.py?confId=7856')


cset = addSet('XCIX Congresso Nazionale della Societ&agrave; Italiana di Fisica',
              'Trieste (Italia)', '23/09/2013', '27/09/2013',
              'http://www.sif.it/attivita/congresso/xcix')
c1 = gContribution('plasduino: an inexpensive, general purpose data acquisition framework for didactic experiments', cset.Conference)
c2 =  gContribution('The Fermi Large Area Telescope',
                    cset.Conference, invited = True)
cset.add(c1)
cset.add(c2)


add('The Silicon Strip Tracker of the Fermi Large Area Telescope: the first 5 years',
    'Vertex 2013', 'Lake Starnberg (Germany)', '16/09/2013', '20/09/2013',
    'http://vertex2013.depfet.org/', invited = True)


add('The Fermi Large Area Telescope',
    'INFN-IHEP Meeting on Cosmic Ray Physics',
    'LNGS', '16/09/2013', '17/09/2013',
    'http://agenda.infn.it/conferenceDisplay.py?confId=6741',
    invited = True)


add('Il Cielo dei Raggi Gamma',
    'Fisica 2010&ndash;2020: Congresso di Dipartimento',
    'Pisa', '17/04/2013', '17/04/2013',
    'http://www.df.unipi.it/content/generic/%5Byy%5D%5Bmm%5D%5Bdd%5D/congressino-2013')


add('The Fermi Large Area Telescope at Launch+4',
    'Spacepart 2012',
    'CERN (Geneve, Switzerland)', '05/11/2012', '07/11/2012',
    'http://indico.cern.ch/conferenceDisplay.py?confId=197799',
    invited = True)


cset = addSet('Fermi Symposium 2012', 'Monterey (California, USA)',
              '28/10/2012', '02/11/2012',
              'http://fermi.gsfc.nasa.gov/science/mtgs/symposia/2012/')
c1 = gContribution('The Fermi Large Area Telescope On Orbit: Validation and '
                   'Calibration of the Instrument Response', cset.Conference)
c2 =  gContribution('Pass 8: toward the full realization of the Fermi LAT '
                    'scientific potential', cset.Conference, poster = True)
cset.add(c1)
cset.add(c2)


add('The Fermi Large Area Telescope at L+4',
    'First International HERD Workshop',
    'Beijing (China)', '17/10/2012', '18/10/2012',
    'http://indico.ihep.ac.cn/conferenceDisplay.py?confId=2838',
    invited = True)


add('Fermi LAT overview and performance',
    'Fermi summer school 2012',
    'Lewes (Delaware, USA)', '29/05/2012', '08/06/2012',
    'http://fermi.gsfc.nasa.gov/science/mtgs/summerschool/2012/',
    notes = 'series of invited lectures')


add('The prolonged Fermi mission',
    'AGILE 9th Science Workshop',
    'Frascati (Roma, Italy)', '16/04/2012', '17/04/2012',
    'http://www.asdc.asi.it/9thagilemeeting/index.php',
    invited = True)


add('The silicon strip tracker of the Fermi LAT: performance '
    'after three years of operation in space',
    '8th Hiroshima Symposium',
    'Taipei (Taiwan)', '05/12/2011', '08/12/2011',
    'http://www-hep.phys.sinica.edu.tw/~hstd8/')


add('Fermi Gamma-ray Space Telescope science highlights',
    '13th ICATPP Conference',
    'Villa Olmo (Como, Italy)', '03/10/2011', '07/10/2011',
    'http://villaolmo.mib.infn.it/home',
    invited = True)


add('The silicon strip tracker of the Fermi Large Area Telescope',
    'RD11 Conference',
    'Firenze', '06/07/2011', '08/07/2011',
    'http://rd11.fi.infn.it/RD11_Home.html')


cset = addSet('23rd Rencontres de Blois', 'Ch&acirc;teau Royal de Blois',
              '29/05/2011', '03/06/2011',
              'http://confs.obspm.fr/Blois2011/')
c1 = gContribution('Recent highlights from the Fermi Large Area Telescope',
                   cset.Conference, invited = True)
c2 = gContribution('Dark Matter indirect searches and tests of Lorentz '
                   'invariance violation with the Fermi LAT', cset.Conference,
                   invited = True)
cset.add(c1)
cset.add(c2)


cset = addSet('Fermi Symposium 2011', 'Roma (Italy)',
              '09/05/2011', '12/05/2011',
              'http://fermi.gsfc.nasa.gov/science/mtgs/symposia/2011/')
c1 = gContribution('Pass 8. A comprehensive revision of the Fermi LAT '
                   'event-level analysis', cset.Conference, poster = True)
c2 = gContribution('The Fermi LAT Calorimeter as a gamma-ray telescope',
                   cset.Conference, poster = True)
cset.add(c1)
cset.add(c2)


add('Cosmic rays and mark matter searches with Fermi',
    'Les Rencontres de Physique de la Vall&eacute;e d\'Aoste',
    'La Thuile (Italy)', '27/02/2011', '05/03/2011',
    'http://www.pi.infn.it/lathuile/lathuile_2011.html')


add('The Fermi Large Area Telescope: highlights from the first two years in '
    'orbit',
    'DICE 2010',
    'Castiglioncello (Italy)', '13/09/2010', '17/09/2010',
    'http://mail.df.unipi.it/~elze/DICE2010.html',
    invited = True)


add('Measurement of the cosmic-ray electron spectrum with the Fermi LAT',
    '22nd European Cosmic-ray Symposium',
    'Turku (Finland)', '03/08/2010', '06/08/2010',
    'http://ecrs2010.utu.fi/',
    invited = True)


add('Fermi-LAT data monitoring',
    'Meeting Nazionale sull\'analisi dei dati dell\'osservatorio Fermi-LAT',
    'Frascati', '01/10/2009', '02/10/2009',
    'http://www.asdc.asi.it/fermimeeting/announcement.php')


add('Experimental review of high-energy electron/positron and '
    'proton/antiproton spectra',
    'TeV Particle Astrophysics 2009',
    'SLAC (Menlo Park, USA)', '13/07/2009', '17/07/2009',
    'http://www-conf.slac.stanford.edu/tevpa09/',
    invited = True)


add('The Fermi LAT: highlights after one year in orbit and '
    'measurement of the cosmic-ray electron spectrum',
    'Searching for the Origins of Cosmic Rays',
    'Trondheim (Norway)', '15/06/2009', '18/06/2009',
    'http://web.phys.ntnu.no/~mika/socor.html')


add('Observation of the high-energy cosmic-ray electron spectrum with '
    'Fermi and implications for dark matter scenarios',
    'New Lights on Dark Matter',
    'Perimeter Institute (Waterloo, Canada)', '11/06/2009', '13/06/2009',
    'http://www.perimeterinstitute.ca/en/Events/New_Lights_on_Dark_Matter/'
    'New_Lights_on_Dark_Matter/',
    invited = True)


add('The Fermi Large Area Telescope as a high-energy electron detector',
    'RICAP 2009',
    'Villa Mondragone (Monte Porzio Catone, Roma)', '13/05/2009', '15/05/2009',
    'http://ricap09.roma2.infn.it/',
    invited = True)


add('The Fermi gamma-ray space telescope: design, construction, '
    'launch and early science results',
    'CERN Detector Seminar',
    'CERN (Geneve, Switzerland)', '20/03/2009', None,
    'http://indico.cern.ch/conferenceDisplay.py?confId=54525',
    invited = True)


add('GRB observations with Fermi',
    'Rencontres de Moriond on Very High-Energy Phenomena in the Universe',
    'La Thuile (Italy)', '01/02/2009', '08/02/2009',
    'http://moriond.in2p3.fr/J09/')


add('The GLAST Large Area Telescope',
    '8th International Conference on Position Sensitive Detectors',
    'Glasgow (Scotland)', '01/09/2008', '05/09/2008',
    'http://www.psd8.physics.gla.ac.uk/index.php')


add('LAT ground calibration: the test campaign',
    'Astrofisica Gamma dallo Spazio in Italia: AGILE e GLAST',
    'Frascati (Roma, Italy)', '02/07/2007', '03/07/2007',
    'http://old.inaf.it/news_cartella/Astrofisica-gamma-dallo-Spazio-in-Italia/'
    '?noredirect=1')


add('Pyhton nell\'esperimento Gamma-Ray Large Area Space Telescope',
    'PyCon Uno',
    'Firenze (Italy)', '09/06/2007', '10/06/2007',
    'http://www.pycon.it/pycon1')


add('The online monitor for the GLAST Calibration Unit beam test',
    'SciNeGHE 2012',
    'Portoferraio (Isola d\'Elba)', '20/06/2006', '22/06/2006',
    'http://glast.pi.infn.it/Elba06/Elba06.html',
    poster = True)


add('The Gamma-ray Large Area Space Telescope: an astro-particle '
    'mission to explore the high-energy sky',
    'IEEE Nuclear Science Symposium',
    'San Juan (Puerto Rico)', '23/10/2005', '27/10/2005',
    'http://www.nss-mic.org/2005/')


add('Highlights and memorabilia from GLAST at INFN-Pisa',
    'GLAST LAT Tracker Construction Workshop',
    'Castelfalfi (Firenze, Italy)', '23/09/2005', None,
    'http://glast.pi.infn.it/celebration/celebration.html')


add('Status of the GLAST tracker construction',
    '5th AGILE Science Workshop',
    'Roma (Italy)', '02/02/2005', None,
    'http://www.fisica.uniroma2.it/~tovastro/ann/050111-agile.html')


add('The silicon-strip tracker of the Large Area Telescope',
    'IEEE Nuclear Science Symposium',
    'Roma (Italy)', '16/10/2004', '22/10/2004',
    'http://nss-mic-rtsd-2004.df.unipi.it/nsshome2004.html')


add('The GLAST silicon tracker construction',
    'RESMDD04',
    'Firenze (Italy)', '10/10/2004', '13/10/2004',
    'http://cern.ch/resmdd')


add('The silicon tracker for the GLAST Mini-tower',
    'Frontier Science: Physics and Astrophysics in Space',
    'Villa Mondragone (Monte Porzio Catone, Italy)', '14/06/2004', '19/06/2004',
    #'',
    poster = True)


add('A gas pixel detector for x-ray polarimetry',
    '9th Topical Seminar on Innovative Particle and Radiation Detectors',
    'Siena (Italy)', '23/05/2004', '26/05/2004',
    'http://www.bo.infn.it/sminiato/siena04.html')


add('A novel gaseus x-Ray polarimeter: data analysis and simulation',
    'Astronomical Telescopes and Instrumentation',
    'Waikoloa (Hawaii, USA)', '22/08/2002', '28/08/2002',
    'http://spie.org/x13667.xml')


add('The silicon strip tracker of the Gamma-ray Large Area Space Telescope',
    '9th European Symposium on Semiconductor Detectors',
    'Schloss Elmau (Germany)', '23/06/2002', '27/06/2002',
    'http://www.hll.mpg.de/elmau',
    poster = True)

"""


# Definition of the page menu.
#
MENU = PageMenu()
MENU.add_entry('Home', 'index.html')
MENU.add_entry('Curriculum vit&aelig;', 'cv.html')
MENU.add_entry('Publications', 'publications.html', ORCID().work_list_html)
MENU.add_entry('Presentations', 'talks.html', CONFERENCE_LIST.html)
MENU.add_entry('About me', 'aboutme.html')
MENU.add_entry('Links', 'links.html')
MENU.add_entry('Miscellanea', 'misc.html')
MENU.add_entry('Didattica', 'teaching.html')
MENU.add_entry('Private area', 'private')


def page_template() -> str:
    """Create the basic template for all the HTML pages in the website.

    The function is reading the basic template in the html file in the contents
    folder and fillin-in all the runtime information that can be calculated
    once and forever at the beginning, such as the last update. The template can
    then be interpolated to add the menu and the actual content.

    Maybe this can be memoized?
    """
    text = webpage.read_content('template.html')
    text = text.format(base_title=PAGE_BASE_TITLE,
                       keywords=PAGE_KEYWORDS_STRING,
                       description=PAGE_DESCRIPTION, author=PAGE_AUTHOR,
                       css_target=DEFAULT_CSS_HREF, header=PAGE_HEADER_TEXT,
                       copyright_start=COPYRIGHT_START_YEAR,
                       copyright_end=COPYRIGHT_END_YEAR,
                       last_update=LAST_UPDATE_STRING)
    return text



def _write_page(title: str, target: str, hook=None) -> None:
    """Write a single html page to file.

    This is the main workhorse function to wirte static html web pages.
    """
    logging.info('Processing page "%s"...', title)
    template = page_template()
    menu = HTML.indent(MENU.html(title), 4)
    content = HTML.indent(webpage.read_content(target), 4)
    if hook is not None:
        content = '{}\n{}'.format(content, hook())
    text = template.format(title, menu, title, content)
    output_file_path = webpage.output_file_path(target)
    logging.info('Writing output file to %s...', output_file_path)
    with open(output_file_path, 'w') as output_file:
        output_file.write(text)
    logging.info('Done.')


def write_static_pages():
    """Write all the html pages in the menu to file.
    """
    # Write the static pages driven by the menu.
    for title, (target, hook) in MENU.items():
        if MENU.target_points_to_file(title):
            _write_page(title, target, hook)
    # And write everything else is necessary.
    _write_page('About this website', 'about.html')


def copy_style_sheets():
    """Copy the relevant style sheets from the local source folder to the
    output html folder to be copied on the remote server.
    """
    logging.info('Copying style sheets...')
    for css in STYLE_SHEETS:
        src = os.path.join(webpage.CSS_FOLDER, css)
        dest = os.path.join(webpage.OUTPUT_CSS_FOLDER, css)
        copy(src, dest)


def copy_images(file_formats=('png',)):
    """Copy all the relevant images into the output folder.
    """
    logging.info('Copying images...')
    file_list = []
    for fmt in file_formats:
        file_list = glob.glob(os.path.join(webpage.IMG_FOLDER, '*.%s' % fmt))
    for src in file_list:
        dest = os.path.join(webpage.OUTPUT_IMG_FOLDER, os.path.basename(src))
        copy(src, dest)


def deploy():
    """Deploy the glorious website.
    """
    webpage.create_local_tree()
    write_static_pages()
    copy_style_sheets()
    copy_images()
