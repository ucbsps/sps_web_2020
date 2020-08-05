from django.shortcuts import render
from django.template.loader import render_to_string, TemplateDoesNotExist

from datetime import date

import mariadb

from secrets import MARIADB_USER, MARIADB_PASSWORD, MARIADB_DB
from error_handler import error_500
from file_util import IMAGE_EXTS

def get_potw_dates():

    try:
        db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                  database=MARIADB_DB, host='localhost', port=3306)

        cur = db_conn.cursor()

        cur.execute('SELECT start_date, end_date FROM web2020_potw' +
                    ' WHERE start_date < (SELECT MAX(start_date) FROM web2020_potw)' +
                    ' ORDER BY start_date DESC')

        results = cur.fetchall()

        return [{'start_date': result[0], 'end_date': result[1]} for result in results]

    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

    return None

def get_latest_potw_data():

    try:
        db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                  database=MARIADB_DB, host='localhost', port=3306)

        cur = db_conn.cursor()

        cur.execute('SELECT start_date, end_date, problem, linked_problem, solution, linked_solution' +
                    ' FROM web2020_potw WHERE start_date < current_timestamp()' +
                    ' ORDER BY start_date DESC LIMIT 1')

        results = cur.fetchall()

        for result in results:
            return {'start_date': result[0], 'end_date': result[1],
                    'problem': result[2], 'linked_problem': result[3],
                    'solution': result[4], 'linked_solution': result[5]}

    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

    return None

def get_potw_data(date):

    try:
        db_conn = mariadb.connect(user=MARIADB_USER, password=MARIADB_PASSWORD,
                                  database=MARIADB_DB, host='localhost', port=3306)

        cur = db_conn.cursor()

        cur.execute('SELECT start_date, end_date, problem, linked_problem, solution, linked_solution' +
                    ' FROM web2020_potw WHERE ? BETWEEN start_date AND end_date' +
                    ' AND end_date < (SELECT MAX(end_date) FROM web2020_potw)' +
                    ' ORDER BY start_date DESC', (date,))

        results = cur.fetchall()

        for result in results:
            return {'start_date': result[0], 'end_date': result[1],
                    'problem': result[2], 'linked_problem': result[3],
                    'solution': result[4], 'linked_solution': result[5]}

    except mariadb.Error as e:
        print('DB Error: {}'.format(e))

    return None

def link_html(file):
    if file == None:
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

    if date > date.today():
        return load_potw_current(request)

    potw_data = get_potw_data(date)

    if potw_data == None:
        return load_potw_current(request)

    past_problems = [[problem['start_date'].isoformat(), problem['end_date'].isoformat()]
                     for problem in get_potw_dates()]

    linked_problem = link_html(potw_data['linked_problem'])
    linked_solution = link_html(potw_data['linked_solution'])

    try:
        content = render_to_string('potw_past.html', {'date': date.isoformat(),
                                                      'problem_description': potw_data['problem'],
                                                      'linked_problem': linked_problem,
                                                      'solution_description': potw_data['solution'],
                                                      'linked_solution': linked_solution,
                                                      'past_problems': past_problems})
    except TemplateDoesNotExist:
        return error_500(request)

    return render(request, 'root.html', {'title': 'POTW for {}'.format(date), 'content': content})

def load_potw_current(request):

    potw_data = get_latest_potw_data()

    if potw_data == None:
        return error_500(request)

    past_problems = [[problem['start_date'].isoformat(), problem['end_date'].isoformat()]
                     for problem in get_potw_dates()]

    try:
        content = render_to_string('potw_current.html', {'problem_description': potw_data['problem'],
                                                         'linked_problem': potw_data['linked_problem'],
                                                         'past_problems': past_problems})
    except TemplateDoesNotExist:
        return error_500(request)

    return render(request, 'root.html', {'title': 'SPS POTW', 'content': content})
