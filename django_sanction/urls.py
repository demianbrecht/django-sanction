# vim: ts=4 sw=4 et:
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^logout/$', 'django_sanction.views.logout'), 
    url(r'^login/(\w+)', 'django_sanction.views.login'),
) 
