"""@todo: nscommerceapi docstring"""
import pickle
from suds.client import Client


class NsCommerceApi(object):
    def __init__(
        self,
        app_fn="application",
        cert_fn="certificate",
        toke_fn="usertoken.p"
    ):
        """Create and return the client, along with security headers"""
        self.app_fn = app_fn
        self.cert_fn = cert_fn
        self.toke_fn = toke_fn
        self.client = None


    def connect(self):
        try:
            with open(self.cert_fn, 'r') as cert_file:
                cert = cert_file.read().rstrip()
        except IOError:
            cert = raw_input('\nenter Certificate:\n\t')
        try:
            with open(self.app_fn, 'r') as app_file:
                app = app_file.read().rstrip()
        except IOError:
            app = raw_input('\nenter Application name:\n\t')
        try:
            with open(self.toke_fn, 'r') as toke_file:
                toke = pickle.load(toke_file).rstrip()
        except IOError:
            toke = raw_input('\nenter UserToken:\n\t')
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
