"""
Django view for the homepage

load_home -- load home page
"""

from django.shortcuts import render
from django.template.loader import render_to_string

from os import path
from random import sample
import xml.etree.ElementTree as ET

import mariadb

from secrets import MARIADB_USER, MARIADB_PASSWORD, MARIADB_DB

from db_util import get_value_by_id
from settings import BASE_DIR
from events_page_loader import get_events
from error_handler import error_500
from potw_page_loader import get_latest_potw_data

HOME_IMAGES = [150, 170, 183, 189, 193, 202, 209]

def load_home(request):
    """Returns homepage."""

    image_ids = sample(HOME_IMAGES, 3)
    upcoming_events = get_events(True, count=3)
    potw_data = get_latest_potw_data()

    image_paths = []

    try:
        db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                  database=MARIADB_DB, host='localhost', port=3306)

        cur = db_conn.cursor()

        for image_id in image_ids:
            image_path = get_value_by_id(cur, 'web2020_images', 'img_path', image_id)

            if image_path is not None:
                image_paths.append(image_path)
    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

    if potw_data is not None:
        potw_content = potw_data['problem']
        potw_start = potw_data['start_date']
        potw_end = potw_data['end_date']
    else:
        potw_content = 'See the <a href="/potw">Problem of the Week page</a>.'

    try:
        content = render_to_string('home.html',
                                   {'home_images': image_paths, 'events': upcoming_events,
                                    'potw': potw_content,
                                    'potw_start': potw_start, 'potw_end': potw_end})
    except TemplateDoesNotExist:
        return error_500(request, 'Home')

    try:
        page_tree = ET.ElementTree(ET.fromstring(content))
    except FileNotFoundError:
        return error_500(request)
    except ET.ParseError:
        print('Parse error')
        return error_500(request)

    page_tree_root = page_tree.getroot()

    header_tags = []
    content = ''

    for child in page_tree_root:
        if child.tag == 'head':
            for head_child in child:
                if not head_child.tag == 'title':
                    header_tags.append(ET.tostring(head_child, method='html', encoding='unicode'))
        if child.tag == 'body':
            content = ET.tostring(child, method='html', encoding='unicode')

    header = ''.join(header_tags)

    # remove body tag from content
    content = content.replace('<body>', '').replace('</body>', '')
    # remove whitespace in order to compress content
#    content = content.replace('\n', '').replace('\t', '')
#    header = header.replace('\n', '').replace('\t', '')

    return render(request, 'root.html', {'title': 'Berkeley SPS',
                                         'header': header, 'content': content})
