"""
Django views for static (or mostly static) pages

load_static_page -- render page with content from static_html subdirectory
load_officers -- render officers page
load_index -- load index page (will probably be moved to new file later)
"""

from django.shortcuts import render
from django.template.loader import render_to_string

from os import path
import xml.etree.ElementTree as ET

from settings import BASE_DIR
from error_handler import error_500

def load_static_page(request, page_name):
    """Return response containing rendering of page_name from static_html.

    Arguments
    request -- Django HttpRequest
    page_name -- name of the page to render. .html file with same name should be in static_html folder
    """

    try:
        page_tree = ET.parse(path.join(BASE_DIR, 'sps_web_2020/static_html/{}.html'.format(page_name)))
    except FileNotFoundError:
        return error_500(request)
    except ET.ParseError:
        return error_500(request)

    page_tree_root = page_tree.getroot()

    title = ''
    content = ''

    for child in page_tree_root:
        if child.tag == 'head':
            for head_child in child:
                if head_child.tag == 'title':
                    title = head_child.text
        if child.tag == 'body':
            content = ET.tostring(child)

    # remove body tag from content
    content = content.replace(b'<body>', b'').replace(b'</body>', b'')
    # remove whitespace in order to compress content
    content = content.replace(b'\n', b'').replace(b'\t', b'')
                    
    return render(request, 'root.html', {'title': title, 'content': content.decode()})

def load_officers(request):
    """Returns officers page."""

    return render(request, 'root.html', {'title': 'Officers', 'content': 'Officers'})

def load_index(request):
    """Returns index (homepage)."""

    return load_static_page(request, 'index')
