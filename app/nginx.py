import json
import urllib2
import httplib 
import threading
import signal
import os
import psutil

def reloadNginx():
	for p in psutil.process_iter(attrs=['pid', 'name']):
		if 'nginx' in p.info['name']:
			os.kill(p.pid, signal.SIGHUP)
			