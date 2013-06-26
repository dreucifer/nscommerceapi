#!/usr/bin/env python
from suds.client import Client
import logging, webbrowser
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

def initNSCommerceApi(application, certificate, token):
	"""Create and return the client, along with security headers"""
	wsdl = 'https://ecomapi.networksolutions.com/soapservice.asmx?wsdl'
	
	#Set up the SOAP client based on the nsCommerce WSDl
	client = Client(wsdl)

	#Create security headers and pass them to the client
	headers = client.factory.create('SecurityCredential')
	headers.Application = application
	headers.Certificate = certificate
	headers.UserToken = ''
	client.set_options(soapheaders=headers)

	#send the client back for manipulation
	return client

def getUserKey(certificate, application='Application Name'):
	"""Fetches the login url and userkey for nsCommerce Public Soap API"""

	client = initNSCommerceApi(certificate = certificate, application = application, token = '')

	#Create the request object and pass it to the WSDL method,
	#Store the key in a file and open the login url
	userkey = client.factory.create('UserKeyType')
	response = client.service.GetUserKey(userkey)
	userkey.UserKey = response.UserKey.UserKey
	webbrowser.open(response.UserKey.LoginUrl)
	with open('userkey', 'w+') as userkeyfile:
		userkeyfile.write(userkey.UserKey)
	print "UserKey written to file"


def getUserToken(certificate, application='Application Name'):
	"""docstring for getUserToken"""
	try:
		userkeyfile = open('userkey', 'r')
	except IOError:
		print 'userkey file not found, creating new one'
		getUserKey(certificate, application)
		raw_input("Press Enter after login validation...")
		userkeyfile = open('userkey', 'r')
	
	client = initNSCommerceApi(certificate = certificate, application = application, token = '')

	usertoken = client.factory.create('UserKeyType')
	usertoken.UserKey = userkeyfile.read()
	response = client.service.GetUserToken(UserToken = usertoken)
	with open('usertoken', 'w') as usertokenfile:
		usertokenfile.write(response.UserToken.UserToken)
	print 'UserToken written to file'

if __name__ == "__main__":
	getUserToken(certificate="5fdaa83772dc4753ae3cb33d248c7864", application="AlternatorParts.com")
