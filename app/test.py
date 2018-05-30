import json
import urllib2
import httplib 
import threading
import signal
import os
import psutil
import nginx
import snowglobe
import carehub
import launcher
import time

print carehub.CareHub("jenkins.allocatesoftware.com", 8888).isUp()

print carehub.CareHub("jenkins.allocatesoftware.com", 8808).isUp()

print carehub.CareHub("news.bbc.co.uk", 80).isUp()




def start_up(bn):
    
    try:    
        launcher.launch(bn)

        build()
        nginx.reloadNginx()
    except Exception as e: 
        print "############# Error launching " + bn
        print(e)


def bgl(bn):
   thread = threading.Thread(target=start_up, args=[bn])
   thread.daemon = True                            # Daemonize thread
   thread.start()          



bgl("master-364")

time.sleep(1)
bgl("master-364")

time.sleep(15)
