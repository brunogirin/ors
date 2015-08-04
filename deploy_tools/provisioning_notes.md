Provision a new site
====================

## Required packages

* nginx 1.4.6
* Python 2.7.6
* Git 1.9.1
* pip 7.1.0
* virtualenv 13.1.0
* docopt 0.6.2

e.g., on Ubuntu

`sudo apt-get install nginx git python python-pip upstart`
`sudo pip install virtualenv docopt==0.6.2`

## Nginx Virtual Host config

* see nginx.template.conf
* move and rename to /etc/nginx/sites-available/SITENAME
* create a soft link of the file to /etc/nginx/sites-enabled/SITENAME, e.g. `sudo ln -s /etc/nginx/sites-available/SITENAME /etc/nginx/sites-enabled/SITENAME`
* remove the link to the default site, sudo rm /etc/nginx/sites-enabled/default
* replace SITENAME with, e.g., staging.my-domain.com
* restart nginx with, `sudo service nginx restart`

## Upstart Job

* see gunicorn-upstart.template.conf
* move to /etc/init/gunicorn-SITENAME.conf. Note: the file needs to end with .conf
* replace SITENAME with your site name e.g., staging.my-domain.com
* start gunicorn with, `sudo start gunicorn-SITENAME`
* Other Commands
*    `sudo stop gunicorn-SITENAME`
*    `sudo restart gunicorn-SITENAME`

## Folder structure:

/var/www/SITENAME
└── database
└── source
└── static
└── virtualenv
