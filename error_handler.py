"""
Django views for error handling

Currently handles error codes 404 and 500.
"""

from django.shortcuts import render
from django.template.loader import render_to_string

def error_404(request, *args, **argv):
    """Returns a nice looking error 404 page."""

    content = render_to_string('error_404.html', {'page_name': request.path})

    return render(request, 'root.html', {'title': 'Error 404: Page Not Found', 'content': content})

def error_500(request, *args, **argv):
    """Returns a nice looking error 500 page."""

    return render(request, 'root.html', {'title': 'Error 500: Internal Error',
                                         'content': '<h1 class="content-header">Internal Error</h1>'})
