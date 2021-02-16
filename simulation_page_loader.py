"""
Django views for simulation pages

load_simulation -- render page with content from simulation subdirectory
"""

from django.shortcuts import render
from django.utils.encoding import get_system_encoding

from os import path
from bs4 import BeautifulSoup as bs4

from settings import BASE_DIR
from error_handler import error_500

def load_simulation(request, sim_name):
    """Return response containing rendering of page_name from static_html.

    Arguments
    request -- Django HttpRequest
    sim_name -- name of the simulation to render.
    	.html file with same name should be in simulation folder
    """

    header = ''
    title = ''
    content = ''

    print(path.join(BASE_DIR, 'sps_web_2020/simulations/{}.html'.format(sim_name)))

    try:
        with open(path.join(BASE_DIR, 'sps_web_2020/simulations/{}.html'.format(sim_name)),
                  encoding=get_system_encoding()) as page_file:

            page_soup = bs4(page_file, 'html.parser')

            header = str(page_soup.head)
            title = str(page_soup.title)
            content = str(page_soup.body)
    except FileNotFoundError as e:
        print(e)
        return error_500(request)
    except Exception as e:
        print(e)
        return error_500(request)

    # remove tags from content
    header = header.replace('<head>', '').replace('</head>', '')
    title = title.replace('<title>', '').replace('</title>', '')
    content = content.replace('<body>', '').replace('</body>', '')

    return render(request, 'root.html', {'title': title, 'header': header, 'content': content})
