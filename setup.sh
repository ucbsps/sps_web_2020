#!/bin/bash

python3 -m pip install virtualenv

python3 -m venv venv

venv/bin/pip install django
venv/bin/pip install flup6
venv/bin/pip install pymysql
venv/bin/pip install DBUtils
venv/bin/pip install beautifulsoup4
