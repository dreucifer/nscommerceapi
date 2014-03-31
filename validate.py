#!/usr/bin/env python
from suds.client import Client
import logging, webbrowser, pickle
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
	headers.UserToken = token
	client.set_options(soapheaders=headers)

	#send the client back for manipulation
	return client

def getUserKey(client):
	"""Fetches the login url and userkey for nsCommerce Public Soap API"""

	#Create the request object and pass it to the WSDL method,
	#Store the key in a file and open the login url
	userkey = client.factory.create('UserKeyType')
	response = client.service.GetUserKey(userkey)
	if response.Status != 'Failure':
		userkey.UserKey = response.UserKey.UserKey
		webbrowser.open(response.UserKey.LoginUrl)
		raw_input("Press Enter after login validation...")
		with open('userkey', 'w+') as userkeyfile:
			userkeyfile.write(userkey.UserKey)
		print "UserKey written to file"
	else:
		print response, '\n'
		print '\n\nError:\t', ''.join(error.Message for error in response.ErrorList)


def getUserToken(client):
	"""Fetches the UserToken using the validated UserKey"""
	try:
		userkeyfile = open('userkey', 'r')
	except IOError:
		print 'userkey file not found, creating new one'
		getUserKey(client)
		userkeyfile = open('userkey', 'r')
	
	usertoken = client.factory.create('UserKeyType')
	usertoken.UserKey = userkeyfile.read()
	response = client.service.GetUserToken(UserToken = usertoken)
	if response.Status != 'Failure':
		with open('securityCredential.p', 'w') as credentialfile:
			credential = client.factory.create('SecurityCredential')
			credential.Application = app
			credential.Certificate = cert
			credential.UserToken = response.UserToken.UserToken
			pickle.dump(credential, credentialfile)
		print 'SecurityCredential written to file'

		with open('usertoken.p', 'w') as usertokenfile:
			pickle.dump(response.UserToken.UserToken, usertokenfile)
		print 'UserToken written to file'
	else:
		print '\n\nError:\t', ''.join(error.Message for error in response.ErrorList)

if __name__ == "__main__":
	try:
		with open('certificate', 'r') as certificatefile:
			cert = certificatefile.read().rstrip()
	except IOError:
		cert = raw_input('\nenter Certificate:\n\t')

	try:
		with open('application', 'r') as applicationfile:
			app = applicationfile.read().rstrip()
	except IOError:
		app = raw_input('\nenter Application name:\n\t')
	
	try:
		with open('usertoken.p', 'r') as tokenfile:
			token = pickle.load(tokenfile).rstrip()
	except IOError:
		token = raw_input('\nenter UserToken:\n\t')

	client = initNSCommerceApi(certificate = cert, application = app, token = '')
	getUserToken(client)
