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
from webpage.helpers import copy, memoize
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
    'Pass 8 vs. Pass 7: How Statistically (In)Dependent Are They? '
    '(And Why Should You Care?)',
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
    'ISAPP School 2014: Multi-wavelength and multi-messenger investigation of '
    'the visible and dark Universe',
    'Belgirate (Italy)',
    'http://isapp.school.2014.to.infn.it',
    '2014-07-21', '2014-07-30'
).add_contribution(
    'Review of cosmic-ray and gamma-ray space-based detectors',
    notes='series of invited lectures'
)
CONFERENCE_LIST.add_conference(
    'Astroparticle Physics 2014',
    'Amsterdam (The Netherlands)',
    'http://indico.cern.ch/conferenceDisplay.py?confId=278032',
    '2014-06-23', '2014-06-28'
).add_contribution(
    'The Fermi Large Area Telescope: status and prospects', invited=True
)
CONFERENCE_LIST.add_conference(
    'Mini-workshop sulla fisica astroparticellare al TeV e oltre',
    'Pisa (Italy)',
    'https://agenda.infn.it/conferenceDisplay.py?confId=7856',
    '2014-05-08', '2014-05-09'
).add_contribution(
    'High-energy cosmic-ray and gamma-ray detectors: experimental overview'
)
CONFERENCE_LIST.add_conference(
    'XCIX Congresso Nazionale della Società Italiana di Fisica',
    'Trieste (Italia)',
    'http://www.sif.it/attivita/congresso/xcix',
    '2013-09-23', '2013-09-27'
).add_contribution(
    'plasduino: an inexpensive, general purpose data acquisition framework for '
    'didactic experiments'
).add_contribution(
    'The Fermi Large Area Telescope', invited=True
)
CONFERENCE_LIST.add_conference(
    'Vertex 2013',
    'Lake Starnberg (Germany)',
    'http://vertex2013.depfet.org/',
    '2013-09-16', '2013-09-20'
).add_contribution(
    'The Silicon Strip Tracker of the Fermi Large Area Telescope: '
    'the first 5 years',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'INFN-IHEP Meeting on Cosmic Ray Physics',
    'Laboratori Nazionali del Gran Sasso (Italy)',
    'http://agenda.infn.it/conferenceDisplay.py?confId=6741',
    '2013-09-16', '2013-09-17'
).add_contribution(
    'The Fermi Large Area Telescope', invited=True
)
CONFERENCE_LIST.add_conference(
    'Fisica 2010&ndash;2020: Congresso di Dipartimento',
    'Pisa (Italy)',
    'http://www.df.unipi.it/content/generic/%5Byy%5D%5Bmm%5D%5Bdd%5D/congressino-2013',
    '2013-04-17'
).add_contribution(
    'Il Cielo dei Raggi Gamma'
)
CONFERENCE_LIST.add_conference(
    'Spacepart 2012',
    'CERN (Geneve, Switzerland)',
    'http://indico.cern.ch/conferenceDisplay.py?confId=197799',
    '2012-11-05', '2012-11-07'
).add_contribution(
    'The Fermi Large Area Telescope at Launch+4', invited=True
)
CONFERENCE_LIST.add_conference(
    'Fermi Symposium 2012',
    'Monterey (California, USA)',
    'http://fermi.gsfc.nasa.gov/science/mtgs/symposia/2012/',
    '2012-10-28', '2012-11-02'
).add_contribution(
    'The Fermi Large Area Telescope On Orbit: Validation and Calibration '
    'of the Instrument Response'
).add_contribution(
    'Pass 8: toward the full realization of the Fermi LAT scientific potential',
    poster=True
)
CONFERENCE_LIST.add_conference(
    'First International HERD Workshop',
    'Beijing (China)',
    'http://indico.ihep.ac.cn/conferenceDisplay.py?confId=2838',
    '2012-10-17', '2012-10-18'
).add_contribution(
    'The Fermi Large Area Telescope at L+4', invited=True
)
CONFERENCE_LIST.add_conference(
    'Fermi summer school 2012',
    'Lewes (Delaware, USA)',
    'http://fermi.gsfc.nasa.gov/science/mtgs/summerschool/2012/',
    '2012-05-29', '2012-06-08'
).add_contribution(
    'Fermi LAT overview and performance', notes='series of invited lectures'
)
CONFERENCE_LIST.add_conference(
    'AGILE 9th Science Workshop',
    'Frascati (Roma, Italy)',
    'http://www.asdc.asi.it/9thagilemeeting/index.php',
    '2012-04-16', '2012-04-17'
).add_contribution(
    'The prolonged Fermi mission', invited=True
)
CONFERENCE_LIST.add_conference(
    '8th Hiroshima Symposium',
    'Taipei (Taiwan)',
    'http://www-hep.phys.sinica.edu.tw/~hstd8/',
    '2011-12-05', '2011-12-08'
).add_contribution(
    'The silicon strip tracker of the Fermi LAT: performance after three years '
    'of operation in space'
)
CONFERENCE_LIST.add_conference(
    '13th ICATPP Conference',
    'Villa Olmo (Como, Italy)',
    'http://villaolmo.mib.infn.it/home',
    '2011-10-03', '2011-10-07'
).add_contribution(
    'Fermi Gamma-ray Space Telescope science highlights', invited=True
)
CONFERENCE_LIST.add_conference(
    'RD11 Conference',
    'Firenze (Italy)',
    'http://rd11.fi.infn.it/RD11_Home.html',
    '2011-07-06', '2011-07-08'
).add_contribution(
    'The silicon strip tracker of the Fermi Large Area Telescope'
)
CONFERENCE_LIST.add_conference(
    '23rd Rencontres de Blois',
    'Ch&acirc;teau Royal de Blois (France)',
    'http://confs.obspm.fr/Blois2011/',
    '2011-05-29', '2011-06-03'
).add_contribution(
    'Recent highlights from the Fermi Large Area Telescope', invited=True
).add_contribution(
    'Dark Matter indirect searches and tests of Lorentz-invariance violation '
    'with the Fermi LAT',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'Fermi Symposium 2011',
    'Roma (Italy)',
    'http://fermi.gsfc.nasa.gov/science/mtgs/symposia/2011/',
    '2011-05-09', '2011-05-12'
).add_contribution(
    'Pass 8. A comprehensive revision of the Fermi LAT event-level analysis',
    poster=True
).add_contribution(
    'The Fermi LAT Calorimeter as a gamma-ray telescope', poster=True
)
CONFERENCE_LIST.add_conference(
    'Les Rencontres de Physique de la Vall&eacute;e d\'Aoste',
    'La Thuile (Italy)',
    'http://www.pi.infn.it/lathuile/lathuile_2011.html',
    '2011-02-27', '2011-03-05'
).add_contribution(
    'Cosmic rays and mark matter searches with Fermi'
)
CONFERENCE_LIST.add_conference(
    'DICE 2010',
    'Castiglioncello (Italy)',
    'http://mail.df.unipi.it/~elze/DICE2010.html',
    '2010-09-13', '2010-09-17'
).add_contribution(
    'The Fermi Large Area Telescope: highlights from the first '
    'two years in orbit',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'Meeting Nazionale sull\'analisi dei dati dell\'osservatorio Fermi-LAT',
    'Frascati (Italy)',
    'http://www.asdc.asi.it/fermimeeting/announcement.php',
    '2010-10-01', '2010-10-01'
).add_contribution(
    'Fermi-LAT data monitoring'
)
CONFERENCE_LIST.add_conference(
    '22nd European Cosmic-ray Symposium',
    'Turku (Finland)',
    'http://ecrs2010.utu.fi/',
    '2010-08-03', '2010-08-06'
).add_contribution(
    'Measurement of the cosmic-ray electron spectrum with the Fermi LAT',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'TeV Particle Astrophysics 2009',
    'SLAC (Menlo Park, USA)',
    'http://www-conf.slac.stanford.edu/tevpa09/',
    '2009-07-13', '2009-07-17'
).add_contribution(
    'Experimental review of high-energy electron/positron and '
    'proton/antiproton spectra',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'Searching for the Origins of Cosmic Rays',
    'Trondheim (Norway)',
    'http://web.phys.ntnu.no/~mika/socor.html',
    '2009-06-15', '2009-06-18'
).add_contribution(
    'The Fermi LAT: highlights after one year in orbit and measurement of the '
    'cosmic-ray electron spectrum'
)
CONFERENCE_LIST.add_conference(
    'New Lights on Dark Matter',
    'Perimeter Institute (Waterloo, Canada)',
    'http://www.perimeterinstitute.ca/en/Events/New_Lights_on_Dark_Matter/'
    'New_Lights_on_Dark_Matter/',
    '2009-06-11', '2009-06-13'
).add_contribution(
    'Observation of the high-energy cosmic-ray electron spectrum with Fermi '
    'and implications for dark matter scenarios',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'RICAP 2009',
    'Villa Mondragone (Monte Porzio Catone, Roma)',
    'http://ricap09.roma2.infn.it/',
    '2009-05-13', '2009-05-15'
).add_contribution(
    'The Fermi Large Area Telescope as a high-energy electron detector',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'CERN Detector Seminar',
    'CERN (Geneve, Switzerland)',
    'http://indico.cern.ch/conferenceDisplay.py?confId=54525',
    '2009-03-20'
).add_contribution(
    'The Fermi gamma-ray space telescope: design, construction, launch and '
    'early science results',
    invited=True
)
CONFERENCE_LIST.add_conference(
    'Rencontres de Moriond on Very High-Energy Phenomena in the Universe',
    'La Thuile (Italy)',
    'http://moriond.in2p3.fr/J09/',
    '2009-02-01', '2009-02-08'
).add_contribution(
    'GRB observations with Fermi'
)
CONFERENCE_LIST.add_conference(
    '8th International Conference on Position Sensitive Detectors',
    'Glasgow (Scotland)',
    'http://www.psd8.physics.gla.ac.uk/index.php',
    '2008-09-01', '2008-09-05'
).add_contribution(
    'The GLAST Large Area Telescope'
)
CONFERENCE_LIST.add_conference(
    'Astrofisica Gamma dallo Spazio in Italia: AGILE e GLAST',
    'Frascati (Roma, Italy)',
    'http://old.inaf.it/news_cartella/Astrofisica-gamma-dallo-Spazio-in-Italia',
    '2007-07-02', '2007-07-03'
).add_contribution(
    'LAT ground calibration: the test campaign'
)
CONFERENCE_LIST.add_conference(
    'PyCon Uno',
    'Firenze (Italy)',
    'http://www.pycon.it/pycon1',
    '2007-06-09', '2007-06-10'
).add_contribution(
    'Pyhton nell\'esperimento Gamma-Ray Large Area Space Telescope'
)
CONFERENCE_LIST.add_conference(
    'SciNeGHE 2012',
    'Portoferraio (Isola d\'Elba)',
    'http://glast.pi.infn.it/Elba06/Elba06.html',
    '2006-06-20', '2006-06-22'
).add_contribution(
    'The online monitor for the GLAST Calibration Unit beam test',
    poster=True
)
CONFERENCE_LIST.add_conference(
    'IEEE Nuclear Science Symposium',
    'San Juan (Puerto Rico)',
    'http://www.nss-mic.org/2005/',
    '2005-10-23', '2005-10-27'
).add_contribution(
    'The Gamma-ray Large Area Space Telescope: an astro-particle mission '
    'to explore the high-energy sky'
)
CONFERENCE_LIST.add_conference(
    'GLAST LAT Tracker Construction Workshop',
    'Castelfalfi (Firenze, Italy)',
    'http://glast.pi.infn.it/celebration/celebration.html',
    '2005-09-23'
).add_contribution(
    'Highlights and memorabilia from GLAST at INFN-Pisa'
)
CONFERENCE_LIST.add_conference(
    '5th AGILE Science Workshop',
    'Roma (Italy)',
    'http://www.fisica.uniroma2.it/~tovastro/ann/050111-agile.html',
    '2005-02-02'
).add_contribution(
    'Status of the GLAST tracker construction'
)
CONFERENCE_LIST.add_conference(
    'IEEE Nuclear Science Symposium',
    'Roma (Italy)',
    'http://nss-mic-rtsd-2004.df.unipi.it/nsshome2004.html',
    '2004-10-16', '2004-10-22'
).add_contribution(
    'The silicon-strip tracker of the Large Area Telescope'
)
CONFERENCE_LIST.add_conference(
    'RESMDD 2004',
    'Firenze (Italy)',
    'http://cern.ch/resmdd',
    '2004-10-10', '2004-10-13'
).add_contribution(
    'The GLAST silicon tracker construction'
)
CONFERENCE_LIST.add_conference(
    'Frontier Science: Physics and Astrophysics in Space',
    'Villa Mondragone (Monte Porzio Catone, Italy)',
    None,
    '2004-06-14', '2004-06-19'
).add_contribution(
    'The silicon tracker for the GLAST Mini-tower', poster=True
)
CONFERENCE_LIST.add_conference(
    '9th Topical Seminar on Innovative Particle and Radiation Detectors',
    'Siena (Italy)',
    'http://www.bo.infn.it/sminiato/siena04.html',
    '2004-05-23', '2004-05-26'
).add_contribution(
    'A gas pixel detector for x-ray polarimetry'
)
CONFERENCE_LIST.add_conference(
    'Astronomical Telescopes and Instrumentation',
    'Waikoloa (Hawaii, USA)',
    'http://spie.org/x13667.xml',
    '2002-08-22', '2002-08-28'
).add_contribution(
    'A novel gaseus x-Ray polarimeter: data analysis and simulation'
)
CONFERENCE_LIST.add_conference(
    '9th European Symposium on Semiconductor Detectors',
    'Schloss Elmau (Germany)',
    'http://www.hll.mpg.de/elmau',
    '2002-06-23', '2002-06-27'
).add_contribution(
    'The silicon strip tracker of the Gamma-ray Large Area Space Telescope',
    poster=True
)


# Definition of the page menu.
#
MENU = PageMenu()
MENU.add_entry('Home', 'index.html')
MENU.add_entry('Curriculum vit&aelig;', 'cv.html')
MENU.add_entry('Publications', 'publications.html', ORCID().work_list.html)
MENU.add_entry('Presentations', 'talks.html', CONFERENCE_LIST.html)
MENU.add_entry('About me', 'aboutme.html')
MENU.add_entry('Links', 'links.html')
MENU.add_entry('Miscellanea', 'misc.html')
MENU.add_entry('Didattica', 'teaching.html')
MENU.add_entry('Private area', 'private')


@memoize
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
    for entry in MENU:
        if entry.points_to_file():
            _write_page(entry.title, entry.target, entry.hook)
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
