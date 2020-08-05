from django.contrib import admin
from django.urls import path, re_path, register_converter

from url_date_converter import url_date_converter

from static_page_loader import load_index, load_static_page, load_officers
from events_page_loader import load_events_upcoming_page, load_events_archive_page, load_events_subpage
from potw_page_loader import load_potw, load_potw_current

register_converter(url_date_converter, 'isodate')

urlpatterns = [
    path('', load_index, name='index'),
    re_path(r'^(about_us)$', load_static_page, name='static_about_us'),
    path('(faq)', load_static_page, name='static_faq'),
    re_path(r'^(partners)$', load_static_page, name='static_partners'),
    path('officers', load_officers, name='officers'),
    re_path(r'^(snack_shack)$', load_static_page, name='static_snack_shack'),
    path('events', load_events_upcoming_page, name='events'),
    path('events/archive', load_events_archive_page, name='events_archive'),
    re_path(r'^events/(outreach)$', load_events_subpage, name='events_outreach'),
    re_path(r'^events/(fsl)$', load_events_subpage, name='events_fsl'),
    re_path(r'^events/(ugs)$', load_events_subpage, name='events_ugs'),
    re_path(r'^events/(bbq)$', load_events_subpage, name='events_bbq'),
    path('potw', load_potw_current, name='potw_current'),
    path('potw/<isodate:date>', load_potw, name='potw_past'),
    re_path(r'^(ipt)$', load_static_page, name='static_ipt'),
    re_path(r'^(bpt)$', load_static_page, name='static_bpt'),
    re_path(r'^committee/(projects)$', load_static_page, name='static_committee_projects'),
    re_path(r'^committee/(outreach)$', load_static_page, name='static_committee_outreach'),
    re_path(r'^committee/(website)$', load_static_page, name='static_committee_website'),
]

handler404 = 'error_handler.error_404'
handler500 = 'error_handler.error_500'
