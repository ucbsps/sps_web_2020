"""
Django view for the homepage

load_home -- load home page
"""

from django.shortcuts import render
from django.template.loader import render_to_string, TemplateDoesNotExist

from os import path
from random import sample
import xml.etree.ElementTree as ET

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
    '/static/images/2021-22_pics/mentorship1.jpg',
    '/static/images/2021-22_pics/mentorship2.jpg',
    '/static/images/2021-22_pics/mentorship3.jpg',
    '/static/images/2021-22_pics/mentorship4.jpg',
    '/static/images/2021-22_pics/mentorship5.jpg',
    '/static/images/2021-22_pics/Carnival1.jpg',
    '/static/images/2021-22_pics/Carnival2.jpg',
    '/static/images/2021-22_pics/Carnival3.jpg',
    '/static/images/2021-22_pics/Calday1.jpg',
    '/static/images/2021-22_pics/projects1.jpg',
    '/static/images/2021-22_pics/projects2.jpg',
    '/static/images/2021-22_pics/projects3.jpg',
    '/static/images/2021-22_pics/projects4.jpg',
    '/static/images/2021-22_pics/projects5.jpg',
    '/static/images/2021-22_pics/projects6.jpg',
    '/static/images/2021-22_pics/zonemeet1.jpg',
    '/static/images/2021-22_pics/zonemeet2.jpg',
    '/static/images/2021-22_pics/misc.jpg',
    '/static/images/2021-22_pics/misc2.jpg',
    '/static/images/2021-22_pics/misc3.jpg',
    '/static/images/2021-22_pics/outreach1.jpg',
    '/static/images/2021-22_pics/outreach2.jpg',
    '/static/images/2021-22_pics/outreach3.jpg',
    '/static/images/2021-22_pics/outreach4.jpg',

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

        if len(potw_content) > 200:
            potw_content_words = potw_content.split(' ')
            potw_content = ''
            while len(potw_content) < 200:
                potw_content = ' '.join([potw_content, potw_content_words.pop(0)])
            potw_content = potw_content + ' ...'
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
