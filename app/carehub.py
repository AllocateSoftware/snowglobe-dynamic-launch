import json
import urllib2
import httplib 
import threading
import os
import socket
import time

class CareHub:

	host = ""
	port = 80

	def __init__(self, host, port):
		self.host = host
		self.port = port

	def baseurl(self):
		url = "http://" + self.host
		if self.port != 80:
			url = url + ":" + str(self.port)
		return url

	def isUp(self):
		
		try:
			return urllib2.urlopen(self.baseurl(),timeout=2).getcode() == 200
		except urllib2.URLError as e:
			return False
		except socket.timeout as e:
			return False

	def wait_until_available(self):

		for x in range(0, 100):
			print "Waiting for carehub instance to become available [try " + str(x) + "]"
			if self.isUp():
				return True
			time.sleep(5)
	
		# We waited, it never came up
		raise Exception("Never coming up")