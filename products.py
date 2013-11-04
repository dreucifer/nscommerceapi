#!/usr/bin/env python
# encoding: utf-8
"""@todo: products module docstring"""
import logging
from nscommerceapi import NsCommerceApi

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)

class Products(NsCommerceApi):

    def __init__(self):
        super(Products, self).__init__()
        self.connect()

    def read(self, **kwargs):
        """@todo: Docstring for getproducts.
        :returns: @todo

        """
        client = self.client
        product = kwargs.get("ns_id", [None])[0]
        if product:
            filterlist = client.factory.create('FilterType')
            filterlist.Field = 'ProductId'
            filterlist.Operator.value = 'Equal'
            filterlist.ValueList = str(product)
            response = client.service.ReadProduct(
                DetailSize="Small", FilterList=filterlist)
        else:
            response = client.service.ReadProduct(
                DetailSize="Small")
        if response.Status == "Success":
            print response
        else:
            print response


if __name__ == '__main__':
    PRODUCTS = Products()
    print PRODUCTS.read(product=1787)
