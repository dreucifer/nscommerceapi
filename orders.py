#!/usr/bin/env python
from suds.client import Client
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

wsdl = 'https://ecomapi.networksolutions.com/soapservice.asmx?wsdl'
ns = 'urn:networksolutions:apis'
application = 'AlternatorParts.com'
certificate = '5fdaa83772dc4753ae3cb33d248c7864'
key = 's5P3WnKk76Hqg4QE'
token = 'Fx28JsPa37Wtr4BKf5c6Q9Xqo5ASd2g8'

client = Client(wsdl)
headers = client.factory.create('SecurityCredential')
headers.Application = application
headers.Certificate = certificate
headers.UserToken = token
client.set_options(soapheaders=headers)

#userkeyrequest = client.factory.create('UserKeyType')
#response = client.service.GetUserKey(userkeyrequest)

#usertokenrequest = client.factory.create('UserKeyType')
#usertokenrequest.UserKey = key
#response = client.service.GetUserToken(UserToken = usertokenrequest)

ordernumber = '13585'
trackingnumber = '9405503699300474277884'

filterlist = client.factory.create('FilterType')
filterlist.Field = 'OrderNumber'
filterlist.Operator.value = 'Equal'
filterlist.ValueList = ordernumber

response = client.service.ReadOrder(DetailSize = "Large", FilterList = filterlist)
order = response.OrderList[0]
print order

package = client.factory.create('PackageType')
package.TrackingNumber = trackingnumber

order.Status._OrderStatusId = 4
order.Status.Name = "Shipped"
order.Shipping.PackageList = [ package ]
order.Archived = True

print client.service.UpdateOrder(Order=order)
#else:
#	print "\n\nOrder # %s Archived" % order._OrderNumber

#print client.factory.create('UpdateOrderRequestType')
#print client
