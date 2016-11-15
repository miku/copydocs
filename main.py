#!/usr/bin/env python
# coding: utf-8

"""
Cleanup tasks.
"""

from __future__ import print_function
from gluish.utils import shellout
import gluish
import hashlib
import json
import luigi
import os
import sys

class Task(gluish.BaseTask):
    BASE = './derived'

class FindPages(Task):

    def run(self):
        output = shellout("""
            find mirror -name "*html" |
            grep -v "action" |
            grep -v "Special:" |
            grep -v "User:" |
            grep -E '\([0-9]*\)' |
            grep -v "title=" > {output} """)
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(self.path())

class Sample(Task):
    """
    Create JSON from wiki pages.
    """

    def requires(self):
        return FindPages()

    def run(self):
        output = shellout("python pp.py > {output}")
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path(ext='ldj'))

class DownloadLinkedPDF(Task):
    """
    For each document that has a PDF linked, try to download it.
    """

    def requires(self):
        return Sample()

    def run(self):
        with self.input().open() as handle:
            for line in handle:
                doc = json.loads(line)
                links = doc.get('page', {}).get('linked_pdfs', {})
                for link in links:
                    filename = '%s.pdf' % (hashlib.sha1(link).hexdigest())
                    target = os.path.join('downloads', filename)
                    if not os.path.exists(target):
                        try:
                            output = shellout("""wget -O {output} "{link}" """, link=link)
                            luigi.LocalTarget(output).move(target)
                        except RuntimeError as err:
                            print(err, file=sys.stderr)

    def output(self):
        return luigi.LocalTarget(path=self.path())

if __name__ == '__main__':
    luigi.run()
