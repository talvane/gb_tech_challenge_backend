#!/bin/bash

python manage.py migrate
python manage.py compilemessages
python manage.py createdefaultuser
python manage.py runserver 0.0.0.0:8000
