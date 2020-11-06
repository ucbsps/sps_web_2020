#!/bin/bash

# Get website code and static files
cd /home/p/ph/physics/sps_web_2020
git checkout release
git pull

# Copy static files to website
rsync -rc ~/sps_web_2020/static ~/public_html/

# Copy .htaccess
cp ~/sps_web_2020/.htaccess ~/public_html/.htaccess

# Trigger update of website code
touch ~/public_html/run.fcgi

# Get latest sync code
cd /home/p/ph/physics/sps_web_sync
git checkout release
git pull

# Run sync scripts
venv/bin/python3 download_calendar.py
venv/bin/python3 download_potw.py
