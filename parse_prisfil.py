#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import urllib2
from settings import *
import csv
import StringIO
import codecs
from operator import itemgetter
import argparse
import sys


def get_prisfil_csv(cached=False):
    """
    fetches prisfil data from specified url and saves it to local cache file.
    returns prisfil data from local cache file.
    """
    if not cached or not os.path.exists(PRISFIL_CACHED):
        print "fetching prisfil from {0:s}...".format(PRISFIL_URL)
        try:
            csvdata = urllib2.urlopen(PRISFIL_URL).read()
        except urllib2.URLError:
            print "ERROR: cannot reach %s" % PRISFIL_URL
            sys.exit(-1)
        with open(PRISFIL_CACHED, 'wb') as prisfil:
            prisfil.write(csvdata)
    else:
        print "using cached prisfil '{0:s}'...".format(PRISFIL_CACHED)
        csvdata = open(PRISFIL_CACHED, 'rb').read()
    return StringIO.StringIO(csvdata)


# from https://gist.github.com/eightysteele/1174811
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cached", help="use locally cached prisfil", action="store_true")
    args = parser.parse_args()
    csv_data = get_prisfil_csv(args.cached)
    reader = UnicodeDictReader(csv_data, delimiter='\t', quotechar='"')
    prisfil_data = []
    for i, row in enumerate(reader):
        if not row['price']:
            print row
            row['price'] = -1
        prisfil_data.append((row['title'], float(row['price'])))
    print "\nparsed {0:d} products".format(i)

    for t, p in sorted(prisfil_data, key=itemgetter(1)):
        print u"{0:.<90s}{1:.>10.0f}kr".format(t, p)
