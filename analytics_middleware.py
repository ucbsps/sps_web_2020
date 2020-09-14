"""
Django Middleware for providing MariaDB backed analytics.

For the sps_web_2020 project, assumes that database and tables are created.
"""

from database_pool import database_pool
import db_util

class AnalyticsMiddleware:
    """Django Middleware for providing Pymysql backed analytics."""

    def __init__(self, get_response):
        """Sets response function, connects to database (failing silently)."""
        self.get_response = get_response

        return

    def insert_analytics(self, path, referer, remote_addr, user_agent):
        """Inserts analytics data into database.

        Automatically updates all relevant tables.

        Arguments:
        path -- the url requested without the domain name/server IP
        referer -- HTTP referer (usually the previous url including domain name/server IP)
        remote_addr -- IP address making the request
        user_agent -- HTTP user agent (provided by browser)
        """

        db_conn = database_pool.connection()

        if db_conn is None:
            return

        cur = db_conn.cursor()

        path_id = db_util.load_set_id(cur, 'web2020_pages', 'page_path', path)
        referer_id = db_util.load_set_id(cur, 'web2020_referers', 'referer', referer)
        remote_addr_id = db_util.load_set_id(cur, 'web2020_remote_addrs', 'remote_addr', remote_addr)
        user_agent_id = db_util.load_set_id(cur, 'web2020_user_agents', 'user_agent', user_agent)

        try:
            if (path_id is not None
                and referer_id is not None
                and remote_addr_id is not None
                and user_agent_id is not None):
                cur.execute('INSERT INTO web2020_analytics' +
                            ' (id, remote_addr_id, user_agent_id, referer_id, page_path_id)' +
                            ' VALUES (0, %s, %s, %s, %s)',
                            (remote_addr_id, user_agent_id, referer_id, path_id,))
        except pymysql.Error as e:
            print('DB Error: {}'.format(e))

        cur.close()
        db_conn.close()

        return

    def __call__(self, request):
        """Processes request.

        If the database is connected, logs request information.
        In either case, forwards the request to the next middleware in the stack.
        """

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
