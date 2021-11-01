"""
Mapping of URLs to functions.

urlpatterns contains rules for normal paths, handler404 and handler500 handle errors.
"""

from django.contrib import admin
from django.urls import path, re_path, register_converter

from url_date_converter import url_date_converter

from api import potw_like
from static_page_loader import load_static_page
from events_page_loader import load_events_upcoming_page, load_events_archive_page, load_events_subpage
from potw_page_loader import load_potw, load_potw_current
from home_page_loader import load_home
from simulation_page_loader import load_simulation

register_converter(url_date_converter, 'isodate')

urlpatterns = [
    path('', load_home, name='home'),
    re_path(r'^(about_us)$', load_static_page, name='static_about_us'),
    re_path(r'^(faq)$', load_static_page, name='static_faq'),
    re_path(r'^(partners)$', load_static_page, name='static_partners'),
    re_path(r'(officers)', load_static_page, name='static_officers'),
    re_path(r'(berkeley_discover_initiatives)', load_static_page, name='static_berkeley_discover_initiatives'),
    re_path(r'^(snack_shack)$', load_static_page, name='static_snack_shack'),
    re_path(r'^(study_halls)$', load_static_page, name='static_study_halls'),
    re_path(r'^(mentorship)$', load_static_page, name='static_mentorship'),
    re_path(r'^(svsh)$', load_static_page, name='static_svsh'),
    path('events', load_events_upcoming_page, name='events'),
    path('events/archive', load_events_archive_page, name='events_archive'),
    re_path(r'^events/(outreach)$', load_events_subpage, name='events_outreach'),
    re_path(r'^events/outreach/(basf)$', load_static_page, name='events_outreach_basf'),
    re_path(r'^events/(fsl)$', load_events_subpage, name='events_fsl'),
    re_path(r'^events/(ugs)$', load_events_subpage, name='events_ugs'),
    re_path(r'^events/(bbq)$', load_events_subpage, name='events_bbq'),
    re_path(r'^events/(mentorship)$', load_events_subpage, name='events_mentorship'),
    re_path(r'^events/(general)$', load_events_subpage, name='events_general'),
    re_path(r'^events/(uspt)$', load_static_page, name='static_uspt'),
    re_path(r'^events/(uspt_solutions)$', load_static_page, name='static_uspt_solutions'),
    re_path(r'^events/(uspt_2020)$', load_static_page, name='static_uspt_2020'),
    re_path(r'^events/(uspt_2019)$', load_static_page, name='static_uspt_2019'),
    re_path(r'^events/(uspt_2018)$', load_static_page, name='static_uspt_2018'),
    re_path(r'^events/(uc_hackathon)$', load_static_page, name='static_uc_hackathon'),
    re_path(r'^events/(uc_hackathon_2021)$', load_static_page, name='static_uc_hackathon_2021'),
    re_path(r'^events/(bpt)$', load_static_page, name='static_bpt'),
    re_path(r'^events/(int_bee)$', load_static_page, name='static_int_bee'),
    re_path(r'^events/(int_bee_2020)$', load_static_page, name='static_int_bee_2020'),
    re_path(r'^events/(int_bee_2021)$', load_static_page, name='static_int_bee_2021'),
    re_path(r'^events/(town_halls)$', load_static_page, name='static_town_halls'),
    re_path(r'^committee/(projects)$', load_static_page, name='static_committee_projects'),
    re_path(r'^committee/(outreach)$', load_static_page, name='static_committee_outreach'),
    re_path(r'^committee/(website)$', load_static_page, name='static_committee_website'),
    re_path(r'^committee/(website/debug_setup)$', load_static_page,
            name='static_committee_website_debug_setup'),
    re_path(r'^committee/(website/shell_intro)$', load_static_page,
            name='static_committee_website_shell_intro'),
    re_path(r'^committee/(website/architecture)$', load_static_page,
            name='static_committee_website_architecture'),
    re_path(r'^committee/(website/cal_guide)$', load_static_page,
            name='static_committee_website_cal_guide'),
    path('potw', load_potw_current, name='potw_current'),
    path('potw/<isodate:date>', load_potw, name='potw_past'),
    path('api/potw_like', potw_like, name='api_potw_like'),
    re_path(r'^committee/website/simulation/(springs_1)$', load_simulation,
            name='simulation_springs_1'),
]

handler404 = 'error_handler.error_404'
handler500 = 'error_handler.error_500'
