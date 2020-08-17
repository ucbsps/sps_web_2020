"""
Django view for the homepage

load_home -- load home page
"""

from django.shortcuts import render
from django.template.loader import render_to_string

from os import path
import xml.etree.ElementTree as ET

from settings import BASE_DIR
from error_handler import error_500

def load_home(request):
    """Returns homepage."""

    return render(request, 'root.html', {'title': 'UC Berkeley Society of Physics Students',
                                         'content': 'UC Berkeley Society of Physics Students'})
