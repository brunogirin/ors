#!/usr/bin/python
"""
Installs the OpenTRV Open REST Server. You can install from a local source folder with the "local" command or directly from the github repository using the "remote" command.

Usage: 
  install (local [--source-dir=<source-dir>] | remote ) [--host=<host> --target-dir=<target>]

Options:
  --host=<host>               The host name [default: ors]
  --target-dir=<target>       Install directory [default: /var/www].
  --source-dir=<source-dir>   Source directory, where the git local repository is [default: ]
"""
import os, subprocess, argparse
from docopt import docopt
argv = docopt(__doc__, help=True)
print argv

print 'installing opentrv'

host = argv['--host']
target_dir = argv['--target-dir']
source_dir = argv['--source-dir']

source_dir = os.path.abspath(os.path.expanduser(source_dir))
target_dir = os.path.expanduser(target_dir)
target_dir = os.path.abspath(target_dir)
install_dir = os.path.join(target_dir, host)

print 'host: {}'.format(host)
print 'install_dir: {}'.format(install_dir)
if argv['remote']:
    REPO_URL = 'https://github.com/opentrv/ors'
elif argv['local']:
                                           REPO_URL = source_dir
else:
    raise(Exception())
print 'REPO_URL: {}'.format(REPO_URL)
print

print 'Creating filestructure'
for subfolder in ['database', 'static', 'virtualenv']:
    try:
        dir = os.path.join(install_dir, subfolder)
        print '\tCreating directory: {}'.format(dir)
        os.makedirs(dir)
        print '\tCreated directory: {}'.format(dir)
    except OSError:
        print '\tDirectory already exists: {}'.format(dir)
print

print 'Getting source code'
source_dir = os.path.join(install_dir, 'source')
print 'source_dir: {}'.format(source_dir)
if os.path.exists(os.path.join(source_dir, '.git')):
    print '\tExisting local repository found, calling git fetch'
    os.chdir(source_dir)
    subprocess.call(['git', 'fetch'])
else:
    print '\Existing local repository not found. Cloning from repo: {}'.format(REPO_URL)
    subprocess.call(['git', 'clone', REPO_URL, source_dir])
# get the most up to date commit on the server if installing from remote or from the local source code repo
subprocess.call(['git', 'reset', '--hard', 'origin'])

print 'Updating the settings'
settings_path = os.path.join(source_dir, 'ors/settings.py')
print 'settings_path: {}'.format(settings_path)
with open(settings_path, 'r') as f:
    lines = []
    for line in f:
        if line == "DEBUG = True\n":
            line = "DEBUG = False\n"
        if line == 'DOMAIN = "localhost"\n':
            line = 'DOMAIN = "{}"\n'.format(host)
        lines.append(line)
    x = 'from .secret_key import SECRET_KEY\n'
    if line != x:
        lines.append(x)
with open(settings_path, 'w') as f:
    for l in lines:
        f.write('{}'.format(l))
secret_key_filepath = os.path.join(source_dir, 'ors', 'secret_key.py')
print

print 'Checking for {}'.format(secret_key_filepath)
if os.path.exists(secret_key_filepath) == False:
    print '\t{}: not found, creating'.format(secret_key_filepath)
    import random
    with open(secret_key_filepath, 'w') as f:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        f.write('SECRET_KEY = "{}"'.format(key))
else:
    print '\t{}: found'.format(secret_key_filepath)
print

print 'Setting up the virtualenv'
virtualenv_dir = os.path.join(install_dir, 'virtualenv')
virtualenv_bin_dir = os.path.join(virtualenv_dir, 'bin')
print '\tvirtualenv_dir: {}'.format(virtualenv_dir)
if not os.path.exists(os.path.join(virtualenv_dir, 'bin', 'pip')):
    os.chdir(install_dir)
    subprocess.call(['virtualenv', 'virtualenv'])
os.chdir(source_dir)
subprocess.call([os.path.join(virtualenv_dir, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])
print

print 'Setting up static files'
os.chdir(source_dir)
subprocess.call([os.path.join(virtualenv_bin_dir, 'python'), 'manage.py', 'collectstatic', '--noinput'])
print

print 'Setting up database'
os.chdir(source_dir)
subprocess.call([os.path.join(virtualenv_bin_dir, 'python'), 'manage.py', 'migrate', '--noinput'])
print

print 'Setting up nginx'
print '\tCreating nginx config file'
string_representation = ''
nginx_conf_filepath = '/etc/nginx/sites-available/{}'.format(host)
with open(source_dir + '/deploy_tools/nginx.template.conf', 'r') as f:
    lines = []
    for l in f:
        l = l.replace('SITENAME', host)
        l = l.replace('SITEDIR', install_dir)
        lines.append(l)
with open(nginx_conf_filepath, 'w') as f:
    for line in lines:
        f.write(line)
        string_representation += line
print '{}:'.format(nginx_conf_filepath)
print string_representation
print '\tConfiguring nginx enabled sites'
# print '\tRemoving previous enabled sites'
# NGINX_ENABLED_SITES_DIR = '/etc/nginx/sites-enabled'
# enabled_sites = os.listdir(NGINX_ENABLED_SITES_DIR)
# for site in enabled_sites:
#     print '\t\t Removing {}'.format(os.path.join(NGINX_ENABLED_SITES_DIR, site))
#     os.remove(os.path.join(NGINX_ENABLED_SITES_DIR, site))
print '\tEnabling new nginx config file'
print '\tln -sf {} {}'.format(nginx_conf_filepath, NGINX_ENABLED_SITES_DIR)
subprocess.call(['ln', '-sf', nginx_conf_filepath, NGINX_ENABLED_SITES_DIR])
print '\tservice nginx restart'
subprocess.call(['service', 'nginx', 'restart'])

print 'Setting up gunicorn'
with open(source_dir + '/deploy_tools/gunicorn-upstart.template.conf') as f:
    lines = []
    for line in f:
        line = line.replace('SITENAME', host)
        line = line.replace('SITEDIR', install_dir)
        lines.append(line)
with open(source_dir + '/deploy_tools/gunicorn.conf', 'w') as f:
    for line in lines:
        print line
        f.write(line)
gunicorn_conf_filepath = '/etc/init/gunicorn-{}.conf'.format(host)
print 'gunicorn_conf_filepath: {}'.format(gunicorn_conf_filepath)
print ' '.join(['mv', source_dir + '/deploy_tools/gunicorn.conf', gunicorn_conf_filepath])
subprocess.call(['mv', source_dir + '/deploy_tools/gunicorn.conf', gunicorn_conf_filepath])
print ' '.join(['start', os.path.split(gunicorn_conf_filepath.replace('conf', ''))[1]])
ret = subprocess.call(['start', os.path.split(gunicorn_conf_filepath.replace('.conf', ''))[1]])
if ret != 0:
    print ' '.join(['restart', os.path.split(gunicorn_conf_filepath.replace('.conf', ''))[1]])
    subprocess.call(['restart', os.path.split(gunicorn_conf_filepath.replace('.conf', ''))[1]])

