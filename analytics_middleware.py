import mariadb

import db_util
from secrets import MARIADB_USER, MARIADB_PASSWORD, MARIADB_DB

class AnalyticsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

        try:
            self.db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                           database=MARIADB_DB, host='localhost', port=3306)

            self.db_connected = True
        except mariadb.Error as e:
            print('Error connecting to database: {}'.format(e))

            self.db_conn = None
            self.db_connected = False

        return

    def insert_analytics(self, path, referer, remote_addr, user_agent):

        if not self.db_connected:
            return

        cur = self.db_conn.cursor()

        path_id = db_util.load_set_id(cur, 'web2020_pages', 'page_path', path)
        if path_id is None:
            self.reload_db()
            return

        referer_id = db_util.load_set_id(cur, 'web2020_referers', 'referer', referer)
        if referer_id is None:
            self.reload_db()
            return

        remote_addr_id = db_util.load_set_id(cur, 'web2020_remote_addrs', 'remote_addr', remote_addr)
        if remote_addr_id is None:
            self.reload_db()
            return

        user_agent_id = db_util.load_set_id(cur, 'web2020_user_agents', 'user_agent', user_agent)
        if user_agent_id is None:
            self.reload_db()
            return

        try:
            cur.execute('INSERT INTO web2020_analytics' +
                        ' (id, remote_addr_id, user_agent_id, referer_id, page_path_id)' +
                        ' VALUES (0, ?, ?, ?, ?)',
                        (remote_addr_id, user_agent_id, referer_id, path_id,))
        except mariadb.Error as e:
            print('DB Error: {}'.format(e))
            self.reload_db()
            return

        return

    def reload_db(self):

        if self.db_conn is not None:
            self.db_conn.close()
        self.db_connected = False

        try:
            self.db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                           database=MARIADB_DB, host='localhost', port=3306)

            self.db_connected = True
        except mariadb.Error as e:
            print('Error connecting to database: {}'.format(e))

            self.db_connected = False

        return        

    def __call__(self, request):

        if self.db_conn:

            cur = self.db_conn.cursor()

            remote_addr = request.META['REMOTE_ADDR']
            path = request.path
            user_agent = request.META['HTTP_USER_AGENT']
            if 'HTTP_REFERER' in request.META:
                referer = request.META['HTTP_REFERER']
            else:
                referer = ''

            self.insert_analytics(path, referer, remote_addr, user_agent)

        response = self.get_response(request)

        return response
