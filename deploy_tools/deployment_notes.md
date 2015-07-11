Deploying the site
====================

## Required packages

* Python 2.7.6
* pip 7.1.0
* fabric 1.10.2

e.g., on Ubuntu

    sudo apt-get install python python-pip
    sudo pip install fabric

From inside the deploy_tools directory and on your LOCAL machine run the command,

fab deploy --host=USERNAME@DOMAIN

e.g. fab deploy --host=dvoong@46.101.52.242

* The USERNAME needs to be part of the sudo group or else it won't have permissions.

## Folder structure:

/var/www
   SITENAME
      database
      source
      static
      virtualenv
