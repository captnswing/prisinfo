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


def xmlrpc_test(api_user, api_key):
    proxy = xmlrpclib.ServerProxy(XMLRPC_URL)
    sessionid = proxy.login(api_user, api_key)
    print sessionid
    print proxy.resources(sessionid)
    proxy.endSession(sessionid)


if __name__ == '__main__':
    try:
        api_user = os.environ['MAGENTO_API_USER']
        api_key = os.environ['MAGENTO_API_KEY']
    except KeyError:
        print "environment variables MAGENTO_API_USER and MAGENTO_API_KEY not found."
        sys.exit(-1)
    xmlrpc_test(api_user, api_key)
