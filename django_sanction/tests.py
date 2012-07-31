# vim: ts=4 sw=4 et:
from os.path import dirname
import subprocess

from django.conf import settings
from django_sanction import Provider

settings.configure(
    SECRET_KEY = "UNIT_TEST",
    URL_CONF = "django_sanction.tests",
    DATABASES = { 
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',                      
        }
    },
    AUTHENTICATION_BACKENDS = (
        "django_sanction.backends.AuthenticationBackend",
    ),
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles', 
        "django_sanction",
    ),
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        "django_sanction.middleware.AuthMiddleware",
    ),
    ROOT_URLCONF = "django_sanction.tests",
    SANCTION_PROVIDERS = {
        "localhost": Provider(
            "localhost",
            "421833888173.apps.googleusercontent.com",
            "VueqKFZyz-aoL4rQFleEIT1j",
            "http://localhost/oauth/dialog",
            "http://localhost/oauth/token",
            "http://localhost/api",
            scope=("email",),
        ),
    },
    SANCTION_AUTH_FN = "django_sanction.tests.auth",
)

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import authenticate
from django.core.management import call_command
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.db import models
from django.test import TestCase
from django.test.client import Client
from django.views.generic import TemplateView

from django_sanction.backends import AuthenticationBackend
from django_sanction.models import User
from django_sanction import urls


# a custom authentication method *MUST* be provided in order to
# get the email address
def auth(request, provider, client):
    data = client.request("/me")

    return User.objects.get_or_create(username="test",
        email=data["email"], access_token=client.access_token,
        provider_key=provider.name,
        expires=data.get("expires", -1))[0]


def render_profile(request):
    assert(request.user.resource_endpoint.access_token\
        == request.user.access_token)
    assert(request.user.resource_endpoint.expires != -1)

    return HttpResponse("hello, world")


urlpatterns = patterns("",
    url(r"^o/", include(urls)), 
    url(r"^accounts/profile/$", render_profile),
)


class TestDefaultBackend(TestCase):
    def setUp(self):
        self.server = subprocess.Popen(("python", "%s/test_server.py" % (
            dirname(__file__))))


    def tearDown(self):
        try:
            self.server.kill()
        except: pass


    def testAuthenticate(self):
        for key in settings.SANCTION_PROVIDERS:
            response = self.client.get("/o/auth/%s" % key.lower(),
                HTTP_HOST="unittest")
            self.assertEquals(response.status_code, 302)


    def testCode(self):
        for key in settings.SANCTION_PROVIDERS:
            response = self.client.get("/o/code/%s" % key.lower(),
                HTTP_HOST="unittest", follow=True)


call_command("syncdb", interactive=False)

