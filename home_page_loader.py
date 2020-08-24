"""
Django view for the homepage

load_home -- load home page
"""

from django.shortcuts import render
from django.template.loader import render_to_string, TemplateDoesNotExist

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

# Home images must have a 1.33333 aspect ratio
# Use command
# file in $(find . -name "*.*");
# do [[ "1.33333" == $(exiftool $file | grep "Image Size" | awk '{print $4}' | awk -F'x' '{print $1 / $2}') ]] && echo $file;
# done

HOME_IMAGES = [
    '/static/images/outreach/TO1.JPG',
    '/static/images/outreach/archive/IMG_6732.JPG',
    '/static/images/outreach/archive/IMG_6733.JPG',
    '/static/images/outreach/archive/IMG_6750.JPG',
    '/static/images/outreach/archive/IMG_6753.JPG',
    '/static/images/outreach/archive/IMG_6777.JPG',
    '/static/images/outreach/archive/IMG_6734.JPG',
    '/static/images/outreach/basf/basf1.jpg',
    '/static/images/outreach/basf/basf2.jpg',
    '/static/images/outreach/calapalooza/calapalooza1.jpg',
    '/static/images/outreach/calday/Calday6.JPG',
    '/static/images/outreach/calday/Calday7.JPG',
    '/static/images/outreach/trio/trio1.jpg',
    '/static/images/outreach/trio/trio2.jpg',
    '/static/images/outreach/trio/trio3.jpg',
    '/static/images/outreach/trio/trio4.jpg',
    '/static/images/outreach/IPT_1.jpg',
    '/static/images/outreach/IPT_2.jpg',
    '/static/images/outreach/TO2_cropped.JPG',
    '/static/images/ugs/CaolanJohn.JPG',
    '/static/images/projects/destress/destress1.jpg',
    '/static/images/projects/destress/destress3.jpg',
    '/static/images/projects/destress/destress4.jpg',
    '/static/images/mentorship/mentorship3.jpg',
    '/static/images/mentorship/mentorship7.jpg',
    '/static/images/mentorship/mentorship8.jpg',
]

def load_home(request):
    """Returns homepage."""

    image_paths = sample(HOME_IMAGES, 3)
    upcoming_events = get_events(True, count=3)
    potw_data = get_latest_potw_data()

    if len(upcoming_events) == 0:
        upcoming_events = [{}, {'title': 'No upcoming events'}, {}]

    if potw_data is not None:
        potw_content = potw_data['problem']
        potw_start = potw_data['start_date']
        potw_end = potw_data['end_date']
    else:
        potw_content = 'See the <a href="/potw">Problem of the Week page</a>.'
        potw_start = None
        potw_end = None

    try:
        content = render_to_string('home.html',
                                   {'home_images': image_paths, 'events': upcoming_events,
                                    'potw': potw_content,
                                    'potw_start': potw_start, 'potw_end': potw_end})
    except TemplateDoesNotExist:
        return error_500(request, 'Home')

    try:
        page_tree = ET.ElementTree(ET.fromstring(content))
    except FileNotFoundError as e:
        print(e)
        return error_500(request)
    except ET.ParseError as e:
        print(e)
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
