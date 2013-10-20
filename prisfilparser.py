#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Prisfil Parser
"""
import os
import urllib2
from StringIO import StringIO
from operator import itemgetter
import argparse
import sys
from settings import *
from util import UnicodeDictReader


def get_prisfil_csv(reloading=False):
    """
    fetches prisfil csv data from specified url and saves it to local cache file.
    returns prisfil csv data from local cache file.
    """
    if reloading or not os.path.exists(PRISFIL_CACHED):
        print "fetching prisfil from {0:s}...".format(PRISFIL_URL)
        try:
            csvdata = urllib2.urlopen(PRISFIL_URL).read()
            # get rid of corrupted characters. "UnicodeDecodeError, invalid continuation byte"
            #csvdata = csvdata.replace('\xc3"', '"')
        except urllib2.URLError:
            print "ERROR: cannot reach %s" % PRISFIL_URL
            sys.exit(-1)
        with open(PRISFIL_CACHED, 'wb') as prisfil:
            prisfil.write(csvdata)
    with open(PRISFIL_CACHED, 'rb') as prisfil:
        csvdata = prisfil.read()
    return csvdata


def get_prisfil_data(*args):
    """
    parses the prisfil csv and extracts the interesting fields.
    returns a list of tuples.
    """
    # get csv data
    csv_data = get_prisfil_csv(*args)
    # get rid of corrupted characters. "UnicodeDecodeError, invalid continuation byte"
    csv_data = csv_data.replace('\xc3"', '"')
    # parse csv data
    reader = UnicodeDictReader(StringIO(csv_data), delimiter='\t', quotechar='"')
    # extract interesting fields
    prisfil_data = []
    for i, row in enumerate(reader):
        if not row['price']:
            row['price'] = 1
        prisfil_data.append((row['title'], float(row['price'])))
    return prisfil_data


if __name__ == '__main__':
    # create argument and options parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reload",
                        help="force reload of local cache file",
                        action="store_true")
    args = parser.parse_args()
    # get prisfil data
    prisfil_data = get_prisfil_data(args.reload)
    # pretty print results
    print "\nparsed {0:d} products".format(len(prisfil_data))
    for t, p in sorted(prisfil_data, key=itemgetter(1)):
        print u"{0:.<90s}{1:.>10.0f}kr".format(t, p)
