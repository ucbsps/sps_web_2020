"""
Functions for sending data to and from the frontend, without generating full pages.

potw_like_dislike allows users to rate POTW problems
"""

from django.http import JsonResponse

from datetime import date
from urllib.parse import urlparse

from database_pool import database_pool
from error_handler import error_500
from settings import ALLOWED_HOSTS

def potw_like_dislike(request):
    """Add another POTW like/dislike to the database."""

    if 'HTTP_REFERER' not in request.META:
        # Request not from web browser maybe, or not from POTW page
        return

    referer = urlparse(request.META['HTTP_REFERER'])

    referer_path = referer.path

    if referer_path == '/potw':
        potw_date = str(date.today())
    else:
        potw_date = referer_path.split('/').pop(-1)

    like = False
    dislike = False
    if request.method == 'POST':
        if 'vote' in request.POST:
            if request.POST['vote'] == 'like':
                like = True
            elif request.POST['vote'] == 'dislike':
                dislike = True

    try:
        db_conn = database_pool.connection()
    except Exception as e:
        print('DB Connection Error: {}'.format(e))
        return error_500(request)

    if db_conn is None:
        return error_500(request)

    cur = db_conn.cursor()

    response = {}

    if like:
        try:
            cur.execute('UPDATE web2020_potw SET likes=likes+1 WHERE %s BETWEEN start_date AND end_date',
                        (potw_date,))

            cur.close()

            response['liked'] = True
        except Exception as e:
            print('DB Error: {}'.format(e))
    elif dislike:
        try:
            cur.execute('UPDATE web2020_potw SET likes=likes+1 WHERE %s BETWEEN start_date AND end_date',
                        (potw_date,))

            cur.close()

            response['disliked'] = True
        except Exception as e:
            print('DB Error: {}'.format(e))
    else:
        try:
            cur.execute('SELECT likes, dislikes FROM web2020_potw' +
                        ' WHERE %s BETWEEN start_date AND end_date',
                        (potw_date,))

            results = cur.fetchall()

            for result in results:
                response['likes'] = result[0]
                response['dislikes'] = result[1]

            cur.close()
        except Exception as e:
            print('DB Error: {}'.format(e))

    db_conn.close()

    return JsonResponse(response)
