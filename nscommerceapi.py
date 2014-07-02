"""@todo: nscommerceapi docstring"""
import os
import pickle
from suds.client import Client


class NsCommerceApi(object):
    def __init__(
        self,
        app_var='NSAPI_APP',
        cert_var='NSAPI_CERT',
        toke_var='NSAPI_TOKEN'
    ):
        """Create and return the client, along with security headers"""
        self.app_var = app_var
        self.cert_var = cert_var
        self.toke_var = toke_var
        self.client = None


    def connect(self):
        try:
            cert = os.environ[self.cert_var]
        except KeyError:
            cert = raw_input('\nEnter Certificate:\n\t')
        try:
            app = os.environ[self.app_var]
        except KeyError:
            app = raw_input('\nEnter Application name:\n\t')
        try:
            toke_fn = os.environ[self.toke_var]
        except KeyError:
            toke_fn = raw_input("Enter UserToken file location:\n\t")
        try:
            with open(toke_fn, 'r') as toke_file:
                toke = pickle.load(toke_file).rstrip()
        except IOError:
            toke = raw_input('\nEnter UserToken:\n\t')

        wsdl = 'https://ecomapi.networksolutions.com/soapservice.asmx?wsdl'

        #Set up the SOAP client based on the nsCommerce WSDl
        client = Client(wsdl)

        #Create security headers and pass them to the client
        headers = client.factory.create('SecurityCredential')
        headers.Application = app
        headers.Certificate = cert
        headers.UserToken = toke
        client.set_options(soapheaders=headers)

        #send the client back for manipulation
        self.client = client
        return client
