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
    AUTH_PROFILE_MODULE = "django_sanction.tests.UserProfile",
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles', 
    ),
    ROOT_URLCONF = "django_sanction.tests",
    SANCTION_PROVIDERS = {
        "localhost": Provider(
            "421833888173.apps.googleusercontent.com",
            "VueqKFZyz-aoL4rQFleEIT1j",
            "http://localhost/oauth/dialog",
            "http://localhost/oauth/token",
            "http://localhost/api",
            scope=("email",),
        ),
    },
    SANCTION_AUTH_FN = "django_sanction.tests.auth",
    SANCTION_GET_USER_FN = "django_sanction.tests.getuser",
)

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
from django_sanction import urls


def auth(request, provider, client):
    return User.objects.get_or_create(username="test",
        email="unit@test.com")[0]


def getuser(user_id):
    return None


urlpatterns = patterns("",
    url(r"^o/", include(urls)), 
)


class CustomUser(object):
    pass


def user_lookup(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return None


class TestBackend(TestCase):
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
                HTTP_HOST="unittest")


call_command("syncdb", interactive=False)

