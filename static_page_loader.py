from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string, TemplateDoesNotExist

import xml.etree.ElementTree as ET

from settings import CONTENT_DIR
from error_handler import error_500

def load_static_page(request, page_name):
    try:
        content = render_to_string('{}.html'.format(page_name))
    except TemplateDoesNotExist:
        return error_500(request, page_name)

    data = ET.fromstring('<content>' + content + '</content>')
    title = ''

    for child in data:
        if child.tag == 'meta' and 'name' in child.attrib:
                if child.attrib['name'] == 'sps:title' and 'content' in child.attrib:
                    title = child.attrib['content']
                    
    return render(request, 'root.html', {'title': title, 'content': content})

def load_officers(request):

    return render(request, 'root.html', {'title': 'Officers', 'content': 'Officers'})

def load_index(request):

    return load_static_page(request, 'index')
