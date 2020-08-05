from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

import xml.etree.ElementTree as ET

from settings import CONTENT_DIR

def error_404(request, *args, **argv):
    content = render_to_string('error_404.html', {'page_name': request.path})

    return render(request, 'root.html', {'title': 'Error 404: Page Not Found', 'content': content})

def error_500(request, *args, **argv):
    return render(request, 'root.html', {'title': 'Error 500: Internal Error',
                                         'content': '<h1 class="content-header">Internal Error</h1>'})
