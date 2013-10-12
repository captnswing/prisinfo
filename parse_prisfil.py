#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import urllib2
import csv
import StringIO
import codecs
from operator import itemgetter
import argparse
import sys

from settings import *


def get_prisfil_csv(reloading=False):
    """
    fetches prisfil data from specified url and saves it to local cache file.
    returns prisfil data from local cache file.
    """
    if reloading or not os.path.exists(PRISFIL_CACHED):
        print "fetching prisfil from {0:s}...".format(PRISFIL_URL)
        try:
            csvdata = urllib2.urlopen(PRISFIL_URL).read()
            # get rid of corrupted characters. "UnicodeDecodeError, invalid continuation byte"
            csvdata = csvdata.replace('\xc3"', '"')
        except urllib2.URLError:
            print "ERROR: cannot reach %s" % PRISFIL_URL
            sys.exit(-1)
        with open(PRISFIL_CACHED, 'wb') as prisfil:
            prisfil.write(csvdata)
    with open(PRISFIL_CACHED, 'rb') as prisfil:
        csvdata = prisfil.read()
    return StringIO.StringIO(csvdata)


# from https://gist.github.com/eightysteele/1174811
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8.
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        n = self.reader.next()
        n = n.encode("utf-8")
        return n


# from https://gist.github.com/eightysteele/1174811
class UnicodeDictReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)
        self.header = self.reader.next()

    def next(self):
        row = self.reader.next()
        vals = [unicode(s, "utf-8") for s in row]
        return dict((self.header[x], vals[x]) for x in range(len(self.header)))

    def __iter__(self):
        return self


def get_prisfil_data(*args):
    """
    parses the prisfil csv and extracts the interesting fields.
    returns a list of tuples.
    """
    # get csv data
    csv_data = get_prisfil_csv(*args)
    # parse csv data
    reader = UnicodeDictReader(csv_data, delimiter='\t', quotechar='"')
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
    parser.add_argument("-r", "--reload", help="force reload of local cache file",
                        action="store_true")
    args = parser.parse_args()
    # get prisfil data
    prisfil_data = get_prisfil_data(args.reload)
    # pretty print results
    print "\nparsed {0:d} products".format(len(prisfil_data))
    for t, p in sorted(prisfil_data, key=itemgetter(1)):
        print u"{0:.<90s}{1:.>10.0f}kr".format(t, p)
