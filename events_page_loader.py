"""
Django views for events and functions supporting those views

get_tag_title -- maps tags (all lowercase) to nicely formatted strings
get_events -- retrieves events from the database
load_events_page -- renders upcoming or past events page
load_events_upcoming_page -- calls load_events_page with upcoming true
load_events_archive_page -- calls load_events_page with upcoming false
load_events_subpage -- renders page for events with a specific tag
"""

from django.shortcuts import render
from django.template.loader import render_to_string, TemplateDoesNotExist

import mariadb

from secrets import MARIADB_USER, MARIADB_PASSWORD, MARIADB_DB

from error_handler import error_500

def get_tag_title(tag):
    """Return a nice title for a tag."""

    if tag == 'outreach':
        return 'Outreach'
    elif tag == 'fsl':
        return 'Faculty-Student Lunch'
    elif tag == 'ugs':
        return 'Undergraduate Seminar'
    elif tag == 'bbq':
        return 'BBQ'
    else:
        return tag

def get_events(upcoming=False, tag=None):
    """Retrieve events from the database, filtering by time and tag.

    Arguments
    upcoming -- bool. True for future events, false for past events.
    tag -- string. If set, filters for events with the tag.
    """

    events = []

    if not tag == None:
        if len(tag) > 0:
            if tag[0] != '#':
                tag = '#' + tag

    try:
        db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                  database=MARIADB_DB, host='localhost', port=3306)

        cur = db_conn.cursor()

        time_clause = 'end_time < current_timestamp()'
        order_clause = 'ORDER BY start_time DESC LIMIT 10'
        if upcoming:
            time_clause = 'end_time > current_timestamp()'
            order_clause = 'ORDER BY start_time ASC LIMIT 10'

        if not tag == None:
            cur.execute('SELECT web2020_events.id, title, description, start_time, end_time,' +
                        ' location, img_path FROM web2020_events LEFT OUTER JOIN web2020_images ON' +
                        ' web2020_events.image_id = web2020_images.id' +
                        ' LEFT OUTER JOIN web2020_events_tags ON' +
                        ' web2020_events.id = web2020_events_tags.event_id' +
                        ' LEFT OUTER JOIN web2020_tags ON' +
                        ' web2020_events_tags.tag_id = web2020_tags.id' +
                        ' WHERE ' + time_clause + ' AND tag=? ' + order_clause,
                        (tag,))
        else:
            cur.execute('SELECT web2020_events.id, title, description, start_time, end_time,' +
                        ' location, img_path FROM web2020_events LEFT OUTER JOIN web2020_images ON' +
                        ' web2020_events.image_id = web2020_images.id' +
                        ' WHERE ' + time_clause + ' ' + order_clause)

        event_results = cur.fetchall()

        for event_result in event_results:
            id = event_result[0]

            img_path = event_result[6]
            if img_path == None:
                cur.execute('SELECT img_path FROM web2020_events' +
                            ' JOIN web2020_events_tags ON' +
                            ' web2020_events.id = web2020_events_tags.event_id' +
                            ' JOIN web2020_tags ON' +
                            ' web2020_events_tags.tag_id = web2020_tags.id' +
                            ' JOIN web2020_images ON' +
                            ' web2020_tags.img_id = web2020_images.id' +
                            ' WHERE web2020_events.id = ?', (id,))

                tag_img_results = cur.fetchall()

                if len(tag_img_results) > 0:
                    img_path = tag_img_results[0][0]

            events.append({'title': event_result[1], 'description': event_result[2],
                           'start_time': event_result[3], 'end_time': event_result[4],
                           'location': event_result[5], 'img_path': img_path})
    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

        events = []

    return events

def load_events_page(request, upcoming=False):
    """Return a render of upcoming events page or archived events page."""

    if upcoming:
        title = 'Upcoming SPS Events'
    else:
        title = 'Past SPS Events'

    try:
        content = render_to_string('events.html', {'events': get_events(upcoming), 'title': title})
    except TemplateDoesNotExist:
        return error_500(request, page_name)
                    
    return render(request, 'root.html', {'title': title, 'content': content})

def load_events_upcoming_page(request):
    """Return a render of upcoming events page."""

    return load_events_page(request, upcoming=True)

def load_events_archive_page(request):
    """Return a render of archived events page."""

    return load_events_page(request, upcoming=False)

def load_events_subpage(request, event_category):
    """Return a render of a page for the set of events with a given tag."""

    title = 'SPS {} Events'.format(get_tag_title(event_category))

    try:
        content = render_to_string('events_tagged.html',
                                   {'upcoming_events': get_events(True, event_category),
                                    'past_events': get_events(False, event_category),
                                    'category': get_tag_title(event_category)})
    except TemplateDoesNotExist:
        return error_500(request, page_name)
                    
    return render(request, 'root.html', {'title': title, 'content': content})
