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

wildcard_suffix = ".snowglobe.allocatesoftware.com"

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    print env
    
    host = env['HTTP_HOST']

    bn = host[0:host.find(".")]


    # bn will contain something like 'master-359'
    if bn in launcher.currently_building:
        # We're currently building. Return the status
        with file(launcher.build_status[bn] + ".html") as f:
            response_text = f.read()
        
    else:
        # Not currently building. Let's do so now.
        with file("build.html") as f:
            response_text = f.read()
        
        thread = threading.Thread(target=start_up, args=[bn])
        thread.daemon = True                            # Daemonize thread
        thread.start()          

    return [response_text]


def start_up(bn):
    
    try:    
        launcher.launch(bn)

        build()
        nginx.reloadNginx()
    except Exception as e: 
        print "############# Error launching " + bn
        print(e)

    
#Build sites for each item
def build():
    items_to_keep = set()

    for description in launcher.snowglobe.list():
        if description.startswith('master-'):
            try:    
                if description not in launcher.currently_building:
                    carehub = launcher.get_carehub(description)
                    this_name = description + wildcard_suffix
                    s = site( this_name, carehub )
                    items_to_keep.add(this_name)
            except Exception as e: 
                print "Error looking at " + description
                print(e)

    # Remove things we no longer need
    files = os.listdir("/etc/nginx/servers/")
    for f in files:
        if f not in items_to_keep:
            os.remove("/etc/nginx/servers/" + f)

#Write out a site definition
def site(host,carehub):
    s = """     # another virtual host using mix of IP-, name-, and port-based configuration
    #
    server {
        listen       80;
        server_name  $HOST;

        location / {            
            proxy_pass $TARGET;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
        }
    }
    """.replace("$HOST",host).replace("$TARGET",carehub.baseurl())

    text_file = open("/etc/nginx/servers/" + host,"w")
    text_file.write(s)
    text_file.close()

    print "####### Created host " + host

    return s

# Initial startup
#
build()
nginx.reloadNginx();

