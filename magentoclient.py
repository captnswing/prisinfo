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


def display_available_resources():
    print "-" * 120
    for r in mclient.resources(sessionid):
        for m in r['methods']:
            print "{:<50} {}".format(m['path'], m['title'])
        print "-" * 120


if __name__ == '__main__':
    try:
        api_user = os.environ['MAGENTO_API_USER']
        api_key = os.environ['MAGENTO_API_KEY']
    except KeyError:
        print "environment variables MAGENTO_API_USER and MAGENTO_API_KEY need to be set."
        sys.exit(-1)

    mclient = xmlrpclib.ServerProxy(XMLRPC_URL)
    sessionid = mclient.login(api_user, api_key)

    display_available_resources()
    prodlist = mclient.call(sessionid, "catalog_product.list")
    for p in prodlist:
        print "{:<30} {}".format(p['sku'], p['name'].encode('utf8'))

    mclient.endSession(sessionid)
