#!/usr/bin/env python
# coding: utf-8

"""
Cleanup tasks.
"""

from gluish.utils import shellout
import gluish
import luigi

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

if __name__ == '__main__':
    luigi.run()
