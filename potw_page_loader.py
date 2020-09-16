"""
Django views for problem of the week and functions supporting those views

get_potw_dates -- return a list of start date and end date pairs for POTW
get_latest_potw_data -- return information on the latest POTW
get_potw_data -- return information on a specific POTW
link_html -- return HTML for embedding an image, embedding a PDF, or linking to something else
load_potw -- render the POTW page for a specific date (used for past POTW)
load_potw_current -- return the POTW page for the latest POTW
"""

from django.shortcuts import render
from django.template.loader import render_to_string, TemplateDoesNotExist

from datetime import date

from database_pool import database_pool
import db_util

from error_handler import error_500
from file_util import IMAGE_EXTS

def get_potw_dates():
    """Return a list of start date and end date pairs for POTWs in the database."""

    try:
        db_conn = database_pool.connection() 
    except Exception as e:
        print('DB Connection Error: {}'.format(e))
        return 

    if db_conn is None:
        return 
    cur = db_conn.cursor()

    try:
        cur.execute('SELECT start_date, end_date FROM web2020_potw' +
                    ' WHERE start_date < (SELECT MAX(start_date) FROM web2020_potw)' +
                    ' ORDER BY start_date DESC')
        results = cur.fetchall()
        cur.close()
    except Exception as e:
        print('DB Error: {}'.format(e))
    
    db_conn.close()

    return [{'start_date': result[0], 'end_date': result[1]} for result in results]



def get_latest_potw_data():
    """Return information on the latest POTW.

    Return value is a dictionary with parameters 'start_date', 'end_date', 'problem',
    'linked_problem', 'solution', and 'linked_solution', with datatypes from the Pymysql connector.
    """

    try:
        db_conn = database_pool.connection()
    except Exception as e:
        print('DB Connection Error: {}'.format(e))
        return 

    if db_conn is None:
        return
    cur = db_conn.cursor()

    try:
        cur.execute('SELECT start_date, end_date, problem, linked_problem, solution, linked_solution' +
                    ' FROM web2020_potw WHERE start_date < current_timestamp()' +
                    ' ORDER BY start_date DESC LIMIT 1')
        results = cur.fetchall()
        for result in results:
            return {'start_date': result[0], 'end_date': result[1],
                    'problem': result[2], 'linked_problem': result[3],
                    'solution': result[4], 'linked_solution': result[5]}
        cur.close()
    except Exception as e:
        print('DB Error: {}'.format(e))

    db_conn.close()

    return 

def get_potw_data(date):
    """Return information on the POTW for given date.

    Return value is a dictionary with parameters 'start_date', 'end_date', 'problem',
    'linked_problem', 'solution', and 'linked_solution', with datatypes from the Pymysql connector.
    """

    try:
        db_conn = database_pool.connection()
        except Exception as e:
            print('DB Connection Error: {}'.format(e))
            return 

    if db_conn is None:
        return

    cur = db_conn.cursor()

    try:
        cur.execute('SELECT start_date, end_date, problem, linked_problem, solution, linked_solution' +
                    ' FROM web2020_potw WHERE %s BETWEEN start_date AND end_date' +
                    ' AND end_date < (SELECT MAX(end_date) FROM web2020_potw)' +
                    ' ORDER BY start_date DESC', (date,))
        results = cur.fetchall()
        for result in results:
            return {'start_date': result[0], 'end_date': result[1],
                    'problem': result[2], 'linked_problem': result[3],
                    'solution': result[4], 'linked_solution': result[5]}
        cur.close()
    except Exception as e:
        print('DB Error: {}'.format(e))

    db_conn.close()
    return None

def link_html(file):
    """Return HTML for embedding an image or PDF or linking other filetypes."""

    if file is None:
        return None

    file_ext = file.split('.')[-1]

    if file_ext in IMAGE_EXTS:
        return '<img src="{}" />'.format(file)
    elif file_ext == 'pdf':
        pdf_size = 'width="100%" height="700px"'
        pdf_open_tag = '<object type="application/pdf" ' + pdf_size + ' data="{}" >'.format(file)
        pdf_close_tag = '</object>'
        pdf_fallback = '<a href="{}">See here.</a>'.format(file)
        return pdf_open_tag + pdf_fallback + pdf_close_tag
    else:
        return '<a href="{}">See here.</a>'.format(file)

def load_potw(request, date):
    """Return the rendered POTW for a specific past date (includes solution)."""

    if date > date.today():
        return load_potw_current(request)

    potw_data = get_potw_data(date)

    if potw_data is None:
        return load_potw_current(request)

    past_problems = [[problem['start_date'].isoformat(), problem['end_date'].isoformat()]
                     for problem in get_potw_dates()]

    linked_problem = link_html(potw_data['linked_problem'])
    linked_solution = link_html(potw_data['linked_solution'])

    try:
        content = render_to_string('potw_past.html',
                                   {'start_date': potw_data['start_date'],
                                    'end_date': potw_data['end_date'],
                                    'problem_description': potw_data['problem'],
                                    'linked_problem': linked_problem,
                                    'solution_description': potw_data['solution'],
                                    'linked_solution': linked_solution,
                                    'past_problems': past_problems})
    except TemplateDoesNotExist:
        return error_500(request)

    return render(request, 'root.html', {'title': 'POTW for {}'.format(date), 'content': content})

def load_potw_current(request):
    """Return the latest rendered POTW (does not include solution)."""

    potw_data = get_latest_potw_data()

    if potw_data is None:
        return error_500(request)

    past_problems = [[problem['start_date'].isoformat(), problem['end_date'].isoformat()]
                     for problem in get_potw_dates()]

    try:
        content = render_to_string('potw_current.html',
                                   {'problem_description': potw_data['problem'],
                                    'start_date': potw_data['start_date'],
                                    'end_date': potw_data['end_date'],
                                    'linked_problem': potw_data['linked_problem'],
                                    'past_problems': past_problems})
    except TemplateDoesNotExist:
        return error_500(request)

    return render(request, 'root.html', {'title': 'SPS POTW', 'content': content})
