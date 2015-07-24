#!/usr/bin/python
"""
Installs the OpenTRV Open REST Server. You can install from a local source folder with the "local" command or directly from the github repository using the "remote" command.

Usage: 
  install (local <source> | remote ) <host> [--target-dir=<target>]

Options:
  --target-dir=<target>  Install directory [default: /var/www].
"""
import os, subprocess, argparse
from docopt import docopt
argv = docopt(__doc__, help=True)
print argv

print 'installing opentrv'

host = argv['<host>']
install_dir = os.path.join(os.path.abspath(os.path.expanduser(argv['--target-dir'])), host)

print 'host: {}'.format(host)
print 'install_dir: {}'.format(install_dir)
if argv['remote']:
    REPO_URL = 'https://github.com/opentrv/ors'
elif argv['local']:
    REPO_URL = os.path.abspath(argv['<source>'])
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
    # os.chdir(source_dir)
# get the most up to date commit on the server if installing from remote or from the local source code repo
# current_commit = subprocess.check_output(['git', 'log', '-n', '1', '--format=%H']).replace('\n', '')
# print '\tcurrent_commit: {}'.format(current_commit)
# print '\tUpdate source code to current commit'
# print subprocess.call(['git', 'reset', '--hard', current_commit])
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
with open(source_dir + '/deploy_tools/nginx.template.conf', 'r') as f:
    lines = []
    for l in f:
        l = l.replace('SITENAME', host)
        l = l.replace('SITEDIR', install_dir)
        lines.append(l)
with open(source_dir + '/deploy_tools/nginx.conf', 'w') as f:
    for line in lines:
        f.write(line)

print 'test5'












# from fabric.contrib.files import append, exists, sed
# from fabric.api import env, local, run
# import random

# def deploy():
#     site_folder = '/var/www/%s' % (env.host)
#     source_folder = site_folder + '/source'
#     _create_directory_structure_if_necessary(site_folder)
#     _get_latest_source(source_folder)
#     _update_settings(source_folder, env.host)
#     _update_virtualenv(source_folder)
#     _update_static_files(source_folder)
#     _update_database(source_folder)

# def _create_directory_structure_if_necessary(site_folder):
#     for subfolder in ('database', 'static', 'virtualenv', 'source'):
#         run('mkdir -p %s/%s' % (site_folder, subfolder))
        
# def _get_latest_source(source_folder):
#     if exists(source_folder + '/.git'):
#         run('cd %s && git fetch' % (source_folder,))
#     else:
#         run('git clone %s %s' %(REPO_URL, source_folder))
#     current_commit = local("git log -n 1 --format=%H", capture=True)
#     run('cd %s && git reset --hard %s' % (source_folder, current_commit))

# def _update_settings(source_folder, site_name):
#     settings_path = source_folder + '/ors/settings.py'
#     sed(settings_path, "DEBUG = True", "DEBUG = False")
#     sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % (site_name,))
#     secret_key_file = source_folder + '/ors/secret_key.py'
#     if not exists(secret_key_file):
#         chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
#         key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
#         append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
#     append(settings_path, '\nfrom .secret_key import SECRET_KEY')

# def _update_virtualenv(source_folder):
#     virtualenv_folder = source_folder + '/../virtualenv'
#     if not exists(virtualenv_folder + '/bin/pip'):
#         run('virtualenv %s' % (virtualenv_folder,))
#     run('%s/bin/pip install -r %s/requirements.txt' % (virtualenv_folder, source_folder))

# def _update_static_files(source_folder):
#     run('cd %s && ../virtualenv/bin/python manage.py collectstatic --noinput' % (source_folder,))

# def _update_database(source_folder):
#     run('cd %s && ../virtualenv/bin/python manage.py migrate --noinput' % (source_folder,))
