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

def extractimages(pdf, directory=None):
    """
    Extract images from a pdf (path), if possible.
    """
    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:
        istream = pdf.find("stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find("endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")
        
        istart += startfix
        iend += endfix
        print("JPG %d from %d to %d" % (njpg, istart, iend))
        jpg = pdf[istart:iend]
        
        filename = os.path.join(directory, "jpg%d.jpg" % njpg)
        print(filename, file=sys.stderr)

        jpgfile = file(filename, "wb")
        jpgfile.write(jpg)
        jpgfile.close()
        
        njpg += 1
        i = iend


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

        output = shellout("""find downloads -name "*pdf" > {output} """)
        luigi.LocalTarget(output).move(self.output().path)

    def output(self):
        return luigi.LocalTarget(path=self.path())

class ImagesFromPDF(Task):
    """
    Extract images from PDF, place them in a separate dir.
    """

    def requires(self):
        return DownloadLinkedPDF()

    def run(self):
        with self.input().open() as handle:
            for line in map(str.strip, handle):
                print(line)
                directory = line.replace(".pdf", "-extractedimages")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                extractimages(open(line, 'rb').read(), directory=directory)

    def output(self):
        return luigi.LocalTarget(path=self.path())

if __name__ == '__main__':
    luigi.run()
