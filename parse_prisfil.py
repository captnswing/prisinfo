#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import urllib2
from settings import *


def get_prisfil_csv():
    """
    fetching prisfil data from specified url and save it to local cache file.
    return prisfil data from local cache file.
    """
    if not os.path.exists(PRISFIL_CACHED):
        print "fetching prisfil from {0:s}...".format(PRISFIL_URL)
        csvdata = urllib2.urlopen(PRISFIL_URL).read()
        with open(PRISFIL_CACHED, 'w') as prisfil:
            prisfil.write(csvdata)
    else:
        print "using cached prisfil '{0:s}'...".format(PRISFIL_CACHED)
        csvdata = open(PRISFIL_CACHED).read()
    return csvdata


if __name__ == '__main__':
    csv_data = get_prisfil_csv()
