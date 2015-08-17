#!/bin/sh
mkdir -p  ../database
python manage.py migrate
python manage.py runserver &
python manage.py test
