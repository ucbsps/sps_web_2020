"""
Django views for static (or mostly static) pages

load_static_page -- render page with content from static_html subdirectory
load_officers -- render officers page
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
    header_tags = []
    content = ''

    for child in page_tree_root:
        if child.tag == 'head':
            for head_child in child:
                if head_child.tag == 'title':
                    title = head_child.text
                else:
                    header_tags.append(ET.tostring(head_child, method='html', encoding='unicode'))
        if child.tag == 'body':
            content = ET.tostring(child, method='html', encoding='unicode')

    header = ''.join(header_tags)

    # remove body tag from content
    content = content.replace('<body>', '').replace('</body>', '')
    # remove whitespace in order to compress content
    content = content.replace('\n', '').replace('\t', '')
    header = header.replace('\n', '').replace('\t', '')
                    
    return render(request, 'root.html', {'title': title, 'header': header, 'content': content})

def load_officers(request):
    """Returns officers page."""

    return render(request, 'root.html', {'title': 'Officers', 'content': 'Officers'})
