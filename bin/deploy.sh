#!/bin/bash

APP_NAME=spacerogue

# Maybe change this install path to something more general
cd /home/$APP_NAME/
git pull

# Unsure if this is needed
#PYTHONPATH=.:.. ./manage.py assets build
sudo pip install -r requirements.txt
sudo supervisorctl restart $APP_NAME

unset PYTHONPATH
