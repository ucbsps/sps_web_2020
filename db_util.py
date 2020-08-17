"""Utilities for interacting with the database.

load_set_id -- tries to find the id corresponding to a value in a table, otherwise adds it.
"""

import mariadb

def load_set_id(cur, table, column, value):
    """Returns find the id corresponding to a value in a table, adding the value if it does not exist.

    Assumes that the table has a column named id, with that column being the primary key (i.e. unique).

    Arguments:
    cur -- a database cursor
    table -- a table name (not SQL injection safe!)
    column -- a column name (not SQL injection safe!)
    value -- the value to look for (SQL injection safe!)
    """

    try:
        cur.execute('SELECT id FROM {} WHERE {}=?'.format(table, column), (value,))
    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

        return None

    ids = cur.fetchall()
    if len(ids) == 0:
        try:
            cur.execute('INSERT INTO {} (id, {}) VALUES(0, ?)'.format(table, column), (value,))
        except mariadb.Error as e:
            print('DB Error: {}'.format(e))

    try:
        cur.execute('SELECT id FROM {} WHERE {}=?'.format(table, column), (value,))
    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

        return None

    ids = cur.fetchall()
    if len(ids) == 0:
        return None

    return ids[0][0]
