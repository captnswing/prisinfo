#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import urllib2
from settings import *
import csv
import StringIO


def get_prisfil_csv():
    """
    fetching prisfil data from specified url and save it to local cache file.
    return prisfil data from local cache file.
    """
    if not os.path.exists(PRISFIL_CACHED):
        print "fetching prisfil from {0:s}...".format(PRISFIL_URL)
        csvdata = urllib2.urlopen(PRISFIL_URL).read()
        with open(PRISFIL_CACHED, 'wb') as prisfil:
            prisfil.write(csvdata)
    else:
        print "using cached prisfil '{0:s}'...".format(PRISFIL_CACHED)
        csvdata = open(PRISFIL_CACHED, 'rb').read()
    return StringIO.StringIO(csvdata)


if __name__ == '__main__':
    csv_data = get_prisfil_csv()
    reader = csv.DictReader(csv_data, delimiter='\t', quotechar='"')
    for i, row in enumerate(reader):
        if i == 0:
            print row.keys()
            print
        if not row['price']:
            continue
        print "{0:.<80s}{1:.>5.2f}kr".format(row['title'], float(row['price']))
