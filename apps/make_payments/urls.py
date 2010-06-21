from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('make_payments.views',                  
    url(r'^$', 'add', name="make_payment.add"),
    url(r'^conf/(?P<id>\d+)/$', 'add_confirm', name="make_payment.add_confirm"), 
    url(r'^(?P<id>\d+)/$', 'view', name="make_payment.view"), 
)