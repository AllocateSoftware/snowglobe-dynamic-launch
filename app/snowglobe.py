import json
import urllib2
import httplib 
import threading
import os


class SnowGlobe:

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

	def clone(self,old,newglobe):
		req = urllib2.Request(self.baseurl() + "/data/globe/" + old + "/clone/"+ newglobe, "", headers = {'accept': 'application/json'})
		return urllib2.urlopen(req).read()

	def set_vars(self,globe, data):
	
		conn = httplib.HTTPConnection(self.host + ":" + str(self.port))

		resp = conn.request('PUT', "/data/globe/"+ globe + "/vars",data)
		r1 = conn.getresponse()
		data1 = r1.read()
		return data1

	def apply(self, globe):
		conn = httplib.HTTPConnection(self.host + ":" + str(self.port))

		resp = conn.request('PUT', "/data/globe/" + globe + "/apply", "")
		r1 = conn.getresponse()
		data1 = r1.read()

		#print r1.status, r1.reason
		#print data1
	
	def list(self):
		items = set()
	
		#Fetch the list
		contents = urllib2.urlopen(self.baseurl() + "/data/globes").read()

		json_contents = json.loads(contents)

		for entry in json_contents:
			items.add(entry['description'])

		return items

	def state(self,globe):
		req = urllib2.Request(self.baseurl() + "/data/globe/" + globe + "/state", headers = {'accept': 'application/json'})
		state =  json.loads(urllib2.urlopen(req).read())
		return state		