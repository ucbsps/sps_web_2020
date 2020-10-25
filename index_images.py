"""
Script to load all images in the static folder into the images table of the database.
"""

import pymysql
import os

from sps_secrets import MARIADB_USER, MARIADB_PASSWORD, MARIADB_DB, MARIADB_HOST
from db_util import load_set_id
from file_util import IMAGE_EXTS

try:
    db_conn = pymysql.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                              database=MARIADB_DB, host=MARIADB_HOST, port=3306, autocommit=True)
except pymysql.Error as e:
    print('Error connecting to database: {}'.format(e))

    exit()

cur = db_conn.cursor()

for (dirpath, dirnames, filenames) in os.walk('static/images'):
    for filename in filenames:
        full_filename = '/{}/{}'.format(dirpath, filename)

        extension = filename.split('.').pop().lower()

        if extension in IMAGE_EXTS:
            load_set_id(cur, 'web2020_images', 'img_path', full_filename)
