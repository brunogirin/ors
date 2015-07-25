#!/usr/bin/python

"""
Usage: 
  orsserver.py start [--host=<host>]
  orsserver.py stop [--host=<host>]
  orsserver.py restart [--host=<host>]

Options:
  --host=<host>  The host namne of the server. [default: 46.101.52.242]
"""

import docopt
import subprocess

argv = docopt.docopt(__doc__, help=True)
print argv

gunicorn_process_name = 'gunicorn-{}'.format(argv['--host'])
print 'gunicorn_process_name: {}'.format(gunicorn_process_name)

if argv['start']:
    subprocess.call(['service', 'nginx', 'start'])
    subprocess.call(['start', gunicorn_process_name])
if argv['stop']:
    subprocess.call(['service', 'nginx', 'stop'])
    subprocess.call(['stop', gunicorn_process_name])
if argv['restart']:
    subprocess.call(['service', 'nginx', 'restart'])
    subprocess.call(['stop', gunicorn_process_name])
