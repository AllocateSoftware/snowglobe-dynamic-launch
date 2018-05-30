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

currently_building = set()
build_status = {}

snowglobe = snowglobe.SnowGlobe("jenkins.allocatesoftware.com", 8808)

# Prevent race
lock = threading.Lock()

def launch(bn):
    global currently_building
    global build_status

    lock.acquire()

    if bn in currently_building:
        print "############# Already starting " + bn
        lock.release()
        return

    currently_building.add(bn)
    lock.release()

    print "############# Starting up " + bn

    build_status[bn] = 'build'
    
      
    build_status[bn] = 'start'
    make(bn)
    # Container will be ready, but app may not have started
    
    build_status[bn] = 'waiting'

    print "############# Waiting for startup of " + bn
    carehub = get_carehub(bn)
    carehub.wait_until_available()

    # remove once it has launched
    del build_status[bn]
    currently_building.remove(bn)
    
    print "############# Startup complete of " + bn   

#Clone and start up system
def make(newglobe):


    snowglobe.clone("ci-template", newglobe)

    # Assume starts with master-
    build_number = newglobe[7:]

    data = """ name="master"
      build=$BUILD_NUMBER""".replace("$BUILD_NUMBER",build_number)

    snowglobe.set_vars(newglobe, data)

    print "############# Snowglobe apply " + newglobe
    snowglobe.apply(newglobe)
    print "############# Snowglobe apply complete:" + newglobe


def get_carehub(globe):
    state = snowglobe.state(globe)
    ip = state['modules']['base']['resources']['docker_container_info']['realtime']['items']['info']['NetworkSettings']['IPAddress']            
    return carehub.CareHub(ip, 8888)
    
