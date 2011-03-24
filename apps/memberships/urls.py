from django.conf.urls.defaults import *

urlpatterns = patterns("memberships.views",
    # memberships
    url(r"^memberships/(?P<id>\d+)/$", "membership_details", name="membership.details"),
    url(r'^memberships/renew/(?P<id>\d)+/$', 'membership_renew', name='membership.renew'),

    # entries
    url(r"^entries/$", "application_entries", name="membership.application_entries"),
    url(r"^entries/(?P<id>\d+)/$", "application_entries", name="membership.application_entries"),
    url(r"^entries/search/$", "application_entries_search", name="membership.application_entries_search"),
    
    # notice
    url(r"^notices/(?P<id>\d+)/email_content/$", "notice_email_content", name="membership.notice_email_content"),

    # application
    url(r"^confirmation/(?P<hash>[\w]+)/$", "application_confirmation", name="membership.application_confirmation"),
    url(r"^(?P<slug>[\w\-]+)/(?P<cmb_id>\d+)?/?$", "application_details", name="membership.application_details"),
    url(r"^(?P<slug>[\w\-]+)/corp-pre/(?P<cmb_id>\d+)?/?$", "application_details_corp_pre", name="membership.application_details_corp_pre"),