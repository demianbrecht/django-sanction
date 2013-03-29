# vim: ts=4 sw=4 et:
from django.conf import settings
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {
        'next_page': settings.LOGIN_URL}),
    url(r'^login/(\w+)', 'django_sanction.views.login'),
) 
