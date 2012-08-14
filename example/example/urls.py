from django.conf.urls import patterns, include, url
import django_sanction.urls
from views import (
	Home,
	Profile,
	Error
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example.views.home', name='home'),
    # url(r'^example/', include('example.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r"^o/", include(django_sanction.urls)),
	url(r"^o/error", Error.as_view()),
	url(r"^$", Home.as_view()),
	url(r"^accounts/profile/$", Profile.as_view()),
)
