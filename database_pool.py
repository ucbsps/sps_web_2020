"""
Database pool

pool -- A PooledDB
    Use pool.connection() to get a connection
    Remember to call close on the cursor and connection after use
"""
import pymysql
from DBUtils.PooledDB import PooledDB

from secrets import MARIADB_USER, MARIADB_DB, MARIADB_PASSWORD, MARIADB_HOST

pool = PooledDB(creator=pymysql, host=MARIADB_HOST, user=MARIADB_USER,
                password=MARIADB_PASSWORD, database=MARIADB_DB,
                autocommit=True, ping=1)
