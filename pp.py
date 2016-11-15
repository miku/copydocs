#!/usr/bin/env python
# coding: utf-8

"""
Scratchpad for getting data out of a single wiki page.

Pages have:

* Abstract (p)
* Main Results of the Study (p)
* Policy Implications as Stated By Author (p)
* Coverage of Study (tables)
* Dataset (tables)

Additional infoboxes:

* Paper (top)
* About the data (bottom)

"""

from bs4 import BeautifulSoup
import json
import sys
import os

KEYMAP = {
    'Discipline': 'discipline',
    'Citation': 'citation',
    'Author(s)': 'authors',
    'Year': 'year',
    'Key Related Studies': 'related',
    'title': 'section_title',
    'Title': 'title',
    'Linked by': 'linked_by',
    'Link(s)': 'links',
    'Industry(ies)': 'industries',
    'Country(ies)': 'countries',
    'Data Analysis Methods': 'data_analysis_methods',
    'Cross Country Study?': 'is_cross_country',
    'Comparative Study?': 'is_comparative_study',
    'Secondary Data Sources': 'secondary_data_sources',
    'Government or policy study?': 'is_government_or_policy_study',
    'Time Period(s) of Collection': 'time_periods_of_collection',
    'Literature review?': 'is_literature_review',
    'Data Collection Methods': 'data_collection_methods',
    'Funder(s)': 'funders',
    'Data Description': 'data_description',
    'Data Type': 'data_type',
}


def abstract(soup):
    """
    Return abstract.

    # PP
    # print(soup.prettify().encode('utf-8'))
    # sys.exit(0)

    # <h3>
    #  <span class="mw-headline" id="Abstract">
    #   Abstract
    #  </span>
    # </h3>
    # <p>
    #  The widespread use of computers and ....
    # </p>
    # <p>
    #  The main purpose of the present ...
    # </p>

    """
    try:
        ps = soup.find('span', {'class': 'mw-headline', 'id': 'Abstract'}).parent.find_next_siblings('p')
        if not ps:
            return ''
        return ' '.join([s.get_text() for s in ps]).strip()
    except AttributeError:
        return ''

def main_results_of_study(soup):
    """
    Main results of study.
    """
    try:
        ps = soup.find('span', {'class': 'mw-headline', 'id': 'Main_Results_of_the_Study'}).parent.find_next_siblings('p')
        if not ps:
            return ''
        return ' '.join([s.get_text() for s in ps]).strip()
    except AttributeError:
        return ''

def policy_implications_as_stated_by_author(soup):
    """
    Policy Implications as Stated By Author.
    """
    try:
        ps = soup.find('span', {'class': 'mw-headline', 'id': 'Policy_Implications_as_Stated_By_Author'}).parent.find_next_siblings('p')
        if not ps:
            return ''
        return ' '.join([s.get_text() for s in ps]).strip()
    except AttributeError:
        return ''

def infobox(soup):
    """
    <table cellpadding="3" class="infobox" style="width:28em;">
    """
    tables = soup.find_all('table', {'class': 'infobox'})
    return tables

def linked_pdfs(soup):
    """
    Only return external PDF for now.
    """
    links = set()
    for link in soup.find_all('a'):
        if link.attrs.get('href', '').startswith('http://www.copyrightevidence.org'):
            continue
        if not link.attrs.get('href', '').startswith('http'):
            continue
        if not link.attrs.get('href', '').endswith('pdf'):
            continue
        links.add(link.attrs.get('href'))
    return list(links)

def boxtodict(box):
    """
    Turn a box into JSON.
    """
    doc = {}
    for i, row in enumerate(box.find_all('tr')):
        if i == 0:
            doc['title'] = row.get_text().strip()
            continue

        rowdoc = breakup(row.get_text())
        doc.update(rowdoc)

    return doc        

def breakup(s):
    """
    Breakup a string from infobox like:

        Key Related Studies:

            Moores and Chang (2006)
            Sims et al. (1996)
            Simpson et al. (1994)
            Liang and Yan (2005)
            Rahim et al. (2001)

    into

        {'Key Related Studies': ['Moores and Chang (2006)', ...]}

    Always returns a dictionary.

    """
    parts = s.split(':', 1)
    if len(parts) == 0:
        return {}
    if len(parts) == 1:
        return {'*': parts}

    sanitized_key = KEYMAP.get(parts[0].strip())
    values = [v.strip() for v in parts[1].strip().split('\n')]

    if sanitized_key.startswith('is_') and len(values) == 1:
        if values[0].lower() == "no":
            values = False
        else:
            values = True

    return {sanitized_key: values}

def htmltodict(soup):
    """
    Parse a wiki HTML page into JSON given a HTML soup.

    """
    # assemble the document
    document = {}

    for box in infobox(soup):
        dd = boxtodict(box)
        if dd.get('title') == 'About the Data':
            # about box (bottom)
            document.update({'about': dd})
        else:
            # top box
            document.update({'info': dd})

    content = {
        'page': {
            'abstract': abstract(soup),
            'results': main_results_of_study(soup),
            'implications': policy_implications_as_stated_by_author(soup),
            'linked_pdfs': linked_pdfs(soup),
        }
    }

    document.update(content)

    return document

if __name__ == '__main__':
    # path = 'mirror/www.copyrightevidence.org/evidence-wiki/index.php/Acilar_(2010).html'
    # path = 'mirror/www.copyrightevidence.org/evidence-wiki/index.php/Angelopoulos_(2012).html'

    with open('derived/default/FindPages/output.tsv') as handle:
        for line in map(str.strip, handle):
            with open(line) as fh:
                content = fh.read()
            soup = BeautifulSoup(content, 'html.parser')

            doc = htmltodict(soup)

            # the URL to the actual wike page
            url = 'http://%s' % (line.replace('mirror/', '').replace('.html', ''))
            doc['page']['url'] = url

            # write to stdout
            print(json.dumps(doc))
