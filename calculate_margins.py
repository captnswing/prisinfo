#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
http://www.magentocommerce.com/api/soap/introduction.html
http://www.magentocommerce.com/api/soap/catalog/catalogProduct/catalog_product.setSpecialPrice.html
"""
import xmlrpclib
from settings import XMLRPC_URL
import os
import sys
import csv
import codecs
import cStringIO
import locale
import time
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')


def fractSec(s):
    # http://www.google.com/search?q=1%20year%20in%20seconds
    y, s = divmod(s, 31556926)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return y, d, h, m, s


def getTotalTimeInMinutes(seconds):
    if not seconds: seconds = 0
    y, d, h, m, s = fractSec(seconds)
    m = m + h * 60 + d * 24 * 60 + y * 365 * 24 * 60
    return "%0.2d:%0.2d" % (m, s)


# from http://stackoverflow.com/a/17245651/41404
class UTF8Recoder:
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)
    def __iter__(self):
        return self
    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8-sig", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()
    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == '__main__':
    #-----------------------------------------------
    # start session
    #-----------------------------------------------
    try:
        api_user = os.environ['MAGENTO_API_USER']
        api_key = os.environ['MAGENTO_API_KEY']
    except KeyError:
        print "environment variables MAGENTO_API_USER and MAGENTO_API_KEY need to be set."
        sys.exit(-1)
    t0 = time.time()
    mclient = xmlrpclib.ServerProxy(XMLRPC_URL)
    sessionid = mclient.login(api_user, api_key)
    csvdata = []
    no_prodinfo = []

    #-----------------------------------------------
    # for all products, get product_info adn calculate margins
    #-----------------------------------------------
    prodlist = mclient.call(sessionid, "catalog_product.list")
    print u"{:<4} {:<10} {:<80} {:>9} {:>9} {:>9}".format("nr", "product_id", "name", "cost", "price", "margin")
    for i, p in enumerate(prodlist, start=1):
        try:
            prodinfo = mclient.call(sessionid, "catalog_product.info", (p["product_id"], "", "", "id"))
        except:
            no_prodinfo.append((p['sku'], p['name']))
            i -= 1
            continue
        pcost = prodinfo.get("cost", 0)
        if pcost:
            pcost = float(pcost)
        pprice = prodinfo.get("price", 0)
        if pprice:
            pprice = float(pprice)
        margin = 0
        if pprice and pcost:
            margin = (pprice - pcost) / pprice * 100
        formated_row = u"{:>4} {:<10} {:<80} {: >9.2f} {: >9.2f} {: >9.2f}".format(i, p["product_id"], p["name"], pcost or 0, pprice or 0, margin)
        row = u"{}\t{}\t{}\t{}\t{}".format(p["product_id"], p["name"], locale.format("%.2f", pcost or 0), locale.format("%.2f", pprice or 0), locale.format("%.2f", margin))
        print formated_row
        csvdata.append(row.split('\t'))

    #-----------------------------------------------
    # write csv file
    #-----------------------------------------------
    with open('margins.csv', 'w') as fp:
        mf = UnicodeWriter(fp, delimiter=',', quoting=csv.QUOTE_ALL)
        mf.writerows(csvdata)

    #-----------------------------------------------
    # fin
    #-----------------------------------------------
    mclient.endSession(sessionid)
    if no_prodinfo:
        print "could not get product info for following items:"
        for pi in no_prodinfo:
            print pi
    print "written {} lines of data to 'margins.csv'".format(len(csvdata))
    print "took {} minutes".format(getTotalTimeInMinutes(time.time()-t0))
