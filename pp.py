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

def abstract(soup):
    """
    Return abstract.
    """
    ps = soup.find('span', {'class': 'mw-headline', 'id': 'Abstract'}).parent.find_next_siblings('p')
    if not ps:
        return ''
    return ' '.join([s.get_text() for s in ps]).strip()

def main_results_of_study(soup):
    """
    Main results of study.
    """
    ps = soup.find('span', {'class': 'mw-headline', 'id': 'Main_Results_of_the_Study'}).parent.find_next_siblings('p')
    if not ps:
        return ''
    return ' '.join([s.get_text() for s in ps]).strip()

def policy_implications_as_stated_by_author(soup):
    """
    Policy Implications as Stated By Author.
    """
    ps = soup.find('span', {'class': 'mw-headline', 'id': 'Policy_Implications_as_Stated_By_Author'}).parent.find_next_siblings('p')
    if not ps:
        return ''
    return ' '.join([s.get_text() for s in ps]).strip()

def infobox(soup):
    """ <table cellpadding="3" class="infobox" style="width:28em;"> """
    tables = soup.find_all('table', {'class': 'infobox'})
    return tables

def breakup(s):
    """
    Breakup a string like:

        Key Related Studies:

            Moores and Chang (2006)
            Sims et al. (1996)
            Simpson et al. (1994)
            Liang and Yan (2005)
            Rahim et al. (2001)

    into

        {'Key Related Studies': ['Moores and Chang (2006)', ...]}

    """
    parts = s.split(':', 1)
    if len(parts) == 0:
        return ''
    if len(parts) == 1:
        return parts
    return {
        parts[0]: [v.strip() for v in parts[1].strip().split('\n')]
    }


if __name__ == '__main__':
    path = 'mirror/www.copyrightevidence.org/evidence-wiki/index.php/Acilar_(2010).html'

    with open(path) as handle:
        html = handle.read()

    soup = BeautifulSoup(html, 'html.parser')

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

    for x in infobox(soup):
        for row in x.find_all('tr'):
            print(breakup(row.get_text()))
            print('----')
        # print(x.prettify())
        # print('----')

    # Lovely.
    # print(json.dumps({
    #     'abstract': abstract(soup),
    #     'results': main_results_of_study(soup),
    #     'implications': policy_implications_as_stated_by_author(soup),
    # }))
