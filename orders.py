#!/usr/bin/env python
# encoding: utf-8
"""Read orders module"""
import logging
import argparse
from nscommerceapi import NsCommerceApi

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)

class Orders(NsCommerceApi):

    def __init__(self):
        super(Orders, self).__init__()
        self.switch = {
            'create': self.create,
            'read': self.read,
            'update': self.update,
            'delete': self.delete,
            }
        self.connect()

    def create(self):
        """Creates a new order via the client using args as a keyword dict of new
        order properties
        """

        pass


    def read(self, **kwargs):
        """Uses a previously generated client and some arguments to """

        client = self.client
        if kwargs:
            order = kwargs.get("order", [None])[0]
            if order is not None:
                order_number = order
                filterlist = client.factory.create('FilterType')
                filterlist.Field = 'OrderNumber'
                filterlist.Operator.value = 'Equal'
                filterlist.ValueList = order_number
                response = client.service.ReadOrder(DetailSize="Large",
                                                    FilterList=filterlist)
            else:
                response = client.service.ReadOrder(DetailSize="Large")
            if response.Status is not 'Failure':
                if hasattr(response, 'OrderList'):
                    return response.OrderList[0]
                else:
                    return None
        else:
            return None


    def update(self, **kwargs):
        """Use client to update order based on parsed_args"""

        client = self.client
        order_number = kwargs.get("order", [None])[0]
        tracking_number = kwargs.get("tracking", [None])
        order = self.read(order=[order_number])
        if (order is not None and tracking_number is not None and
                hasattr(order, 'Status') and hasattr(order, 'Shipping')):
            package = client.factory.create('PackageType')
            package.TrackingNumber = tracking_number
            if getattr(order.Status, '_OrderStatusId') != 4:
                setattr(order.Status, '_OrderStatusId', 4)
                order.Status.Name = "Shipped"
                order.Shipping.PackageList = [package]
                response = client.service.UpdateOrder(Order=order)
                if response.Status is not 'Failed':
                    print response.Status
                    return "Order#: %(order)s Archived" % {
                        'order': order_number}
                else:
                    print 'Update Order Failed'
                    return response
            else:
                return 'Order # %s Already Shipped' % order_number
        else:
            if order == -1:
                return 'Order not found'
            if tracking_number is None:
                return 'No tracking number provided'
            return 'Update Order Failed'


    def delete(self):
        """Delete an order referenced in the arguments via client"""

        pass

if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(description='Takes order and tracking\
            numbers, then adds the tracking number to the order')
    PARSER.add_argument('-o', '--order', nargs=1, type=str,
                        metavar='order_number', required=True,
                        help='Order number to add the tracking number to')
    PARSER.add_argument(
        '-t', '--tracking',
        nargs=1, type=str, default=None, metavar='tracking_number',
        help='Tracking number to add'
        )
    PARSER.add_argument(
        'action', nargs=1, type=str,
        default='read', metavar='action',
        help='CRUD (Create, Read, Update, Delete) action to perform',
        choices=['create', 'read', 'update', 'delete'])
    ARGS = PARSER.parse_args()
    KWARGS = vars(ARGS)
    ORDERS = Orders()
    print ORDERS.switch.get(ARGS.action[0], ORDERS.read)(**KWARGS)
