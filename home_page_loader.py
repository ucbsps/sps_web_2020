"""
Django view for the homepage

load_home -- load home page
"""

from django.shortcuts import render
from django.template.loader import render_to_string

from os import path
import xml.etree.ElementTree as ET

from settings import BASE_DIR
from events_page_loader import get_events
from error_handler import error_500

def load_home(request):
    """Returns homepage."""

    try:
        content = render_to_string('home.html',
                                   {'upcoming_events': get_events(True, count=3)})
    except TemplateDoesNotExist:
        return error_500(request, 'Home')

    try:
        page_tree = ET.ElementTree(ET.fromstring(content))
    except FileNotFoundError:
        return error_500(request)
    except ET.ParseError:
        return error_500(request)

    page_tree_root = page_tree.getroot()

    header_tags = []
    content = ''

    for child in page_tree_root:
        if child.tag == 'head':
            for head_child in child:
                if not head_child.tag == 'title':
                    header_tags.append(ET.tostring(head_child).decode())
        if child.tag == 'body':
            content = ET.tostring(child).decode()

    header = ''.join(header_tags)

    # remove body tag from content
    content = content.replace('<body>', '').replace('</body>', '')
    # remove whitespace in order to compress content
    content = content.replace('\n', '').replace('\t', '')
    header = header.replace('\n', '').replace('\t', '')

    return render(request, 'root.html', {'title': 'UC Berkeley SPS',
                                         'header': header, 'content': content})
