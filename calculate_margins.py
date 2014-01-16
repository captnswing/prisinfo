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
import json


if __name__ == '__main__':
    try:
        api_user = os.environ['MAGENTO_API_USER']
        api_key = os.environ['MAGENTO_API_KEY']
    except KeyError:
        print "environment variables MAGENTO_API_USER and MAGENTO_API_KEY need to be set."
        sys.exit(-1)

    #-----------------------------------------------
    # start session
    #-----------------------------------------------
    mclient = xmlrpclib.ServerProxy(XMLRPC_URL)
    sessionid = mclient.login(api_user, api_key)

    #-----------------------------------------------
    # calculating margins
    #-----------------------------------------------
    prodlist = mclient.call(sessionid, "catalog_product.list")
    print u"{:<4} {:<10} {:<80} {:>9} {:>9} {:>9}".format("nr", "product_id", "name", "cost", "price", "margin")
    for i, p in enumerate(prodlist[:10], start=1):
        prodinfo = mclient.call(sessionid, "catalog_product.info", (p["product_id"], "", "", "id"))
        #print prodinfo.keys()
        pcost = prodinfo.get("cost", 0)
        if pcost:
            pcost = float(pcost)
        pprice = prodinfo.get("price", 0)
        if pprice:
            pprice = float(pprice)
        margin = 0
        if pprice and pcost:
            margin = (pprice - pcost) / pprice * 100
        print u"{:>4} {:<10} {:<80} {: >9.2f} {: >9.2f} {: >9.2f}".format(i, p["product_id"], p["name"], pcost or 0, pprice or 0, margin)

    #-----------------------------------------------
    # end session
    #-----------------------------------------------
    mclient.endSession(sessionid)
