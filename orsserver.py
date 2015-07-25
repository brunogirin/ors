#!/usr/bin/python

"""
Usage: 
  orsserver.py start [--host=<host> --port=<port>]
  orsserver.py stop [--host=<host>]
  orsserver.py restart [--host=<host> --port=<port>]

Options:
  --host=<host>  The host namne of the server. [default: 46.101.52.242]
  --port=<port>  The port number for the HTTP server. [default: 1023]
"""

import docopt
import subprocess
import re

argv = docopt.docopt(__doc__, help=True)
print argv

host = argv['--host']
port = argv['--port']
gunicorn_process_name = 'gunicorn-{}'.format(host)

print 'host: {}'.format(host)
print 'port: {}'.format(port)
print 'gunicorn_process_name: {}'.format(gunicorn_process_name)

NGINX_CONFIG_FILEPATH = '/etc/nginx/sites-available/{}'.format(host)
NGINX_CONFIG_FILEPATH_ENABLED = '/etc/nginx/sites-enabled/{}'.format(host)

def update_nginx_config(port):
    regex = 'listen\s+\d+\s?;$'
    with open(NGINX_CONFIG_FILEPATH, 'rb') as f:
        lines = []
        for line in f:
            if 'listen' in line:
                line = re.sub('\d+', port, line)
            lines.append(line)
    with open(NGINX_CONFIG_FILEPATH, 'wb') as f:
        for line in lines:
            f.write(line)

if argv['start']:
    update_nginx_config(port)
    subprocess.call(['service', 'nginx', 'start'])
    subprocess.call(['start', gunicorn_process_name])
if argv['stop']:
    subprocess.call(['service', 'nginx', 'stop'])
    subprocess.call(['stop', gunicorn_process_name])
if argv['restart']:
    update_nginx_config(port)
    subprocess.call(['service', 'nginx', 'restart'])
    subprocess.call(['restart', gunicorn_process_name])
