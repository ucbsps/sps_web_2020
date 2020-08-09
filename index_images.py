"""
Script to load all images in the static folder into the images table of the database.
"""

import mariadb
import os

from secrets import MARIADB_USER, MARIADB_PASSWORD, MARIADB_DB
from db_util import load_set_id

ALLOWED_TYPES = ['png', 'jpg', 'svg']

try:
    db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                              database=MARIADB_DB, host='localhost', port=3306)
except mariadb.Error as e:
    print('Error connecting to database: {}'.format(e))

    exit()

cur = db_conn.cursor()

for (dirpath, dirnames, filenames) in os.walk('static/images'):
    for filename in filenames:
        full_filename = '/{}/{}'.format(dirpath, filename)

        extension = filename.split('.').pop().lower()

        if extension in ALLOWED_TYPES:
            load_set_id(cur, 'web2020_images', 'img_path', full_filename)
