from django.conf.urls.defaults import *

from notification.views import (notices, mark_all_seen, feed_for_user,
    single, email)

urlpatterns = patterns('',
    url(r'^$', notices, name="notification_notices"),
    url(r'^(\d+)/$', single, name="notification_notice"),
    url(r'^feed/$', feed_for_user, name="notification_feed_for_user"),
    url(r'^mark_all_seen/$', mark_all_seen, name="notification_mark_all_seen"),
    url(r'^(?P<guid>[\d\w-]+)?/$', email, name="notification_email"),
)
