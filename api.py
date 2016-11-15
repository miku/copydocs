#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.simplefilter('ignore', FutureWarning)

from wikitools import wiki
from wikitools import api
import json

if __name__ == '__main__':

    site = wiki.Wiki("http://www.copyrightevidence.org/evidence-wiki/api.php")
    # get all categories
    params = {'action':'query', 'list':'allcategories'}

    # {
    #   "query-continue": {
    #     "allcategories": {
    #       "accontinue": "Methods"
    #     }
    #   },
    #   "query": {
    #     "allcategories": [
    #       {
    #         "*": "Authors"
    #       },
    #       {
    #         "*": "CandidateStudies"
    #       },
    #       {
    #         "*": "Countries"
    #       },
    #       {
    #         "*": "Data Sources"
    #       },

    # get all pages
    params = {'action':'query', 'list':'allpages'}

    # {
    #   "query-continue": {
    #     "allpages": {
    #       "apcontinue": "A._Marvasti"
    #     }
    #   },
    #   "query": {
    #     "allpages": [
    #       {
    #         "ns": 0,
    #         "pageid": 2182,
    #         "title": "1. Relationship between protection (subject matter/term/scope) ..."
    #       },
    #       {
    #         "ns": 0,
    #         "pageid": 2183,
    #         "title": "2. Relationship between creative process and protection - ...?"
    #       },

    # get all images
    params = {'action':'query', 'list':'allimages'}

    # {
    #   "query-continue": {
    #     "allimages": {
    #       "aicontinue": "A_off.png"
    #     }
    #   },
    #   "query": {
    #     "allimages": [
    #       {
    #         "name": "1_off.png",
    #         "title": "File:1 off.png",
    #         "url": "http://www.copyrightevidence.org/evidence-wiki/images/1/10/1_off.png",
    #         "timestamp": "2015-08-21T20:27:23Z",
    #         "descriptionurl": "http://www.copyrightevidence.org/evidence-wiki/index.php/File:1_off.png",
    #         "ns": 6
    #       },

    # get all links
    # very slow, for some reason

    # get all pagepropnames
    params = {'action':'query', 'list':'pagepropnames'}


    request = api.APIRequest(site, params)
    result = request.query()
    print(json.dumps(result))
