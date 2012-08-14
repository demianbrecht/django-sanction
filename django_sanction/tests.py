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
    AUTHENTICATION_USE_CSRF = False, # for most tests
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
        "django_sanction.middleware.ResourceMiddleware",
    ),
    ROOT_URLCONF = "django_sanction.tests",
    OAUTH2_PROVIDERS = ( 
        Provider(
            "localhost",
            "421833888173.apps.googleusercontent.com",
            "VueqKFZyz-aoL4rQFleEIT1j",
            "http://localhost/oauth/dialog",
            "http://localhost/oauth/token",
            "http://localhost/api",
            scope=("email",),
        ),
    ),
)

from django.db import models
import django.contrib.auth.models
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth import authenticate
from django.contrib.auth.models import User as BaseUser
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
from django_sanction.middleware import ResourceMiddleware
from django_sanction import urls



def render_profile(request):
    assert(request.user.resource.access_token\
        == request.user.access_token)
    assert(request.user.resource.expires != -1)

    return HttpResponse("")


def render_home(request):
    return HttpResponse("")

urlpatterns = patterns("",
    url(r"^o/", include(urls)), 
    url(r"^accounts/profile/$", render_profile),
    url(r"^$", render_home),
)


class TestDefaultBackend(TestCase):
    def setUp(self):
        settings.OAUTH2_AUTH_FN = \
            "django_sanction.tests.TestDefaultBackend.auth"
        if hasattr(settings, "OAUTH2_GET_USER_FN"):
            delattr(settings, "OAUTH2_GET_USER_FN")
        if hasattr(settings, "OAUTH2_USER_CLASS"):
            delattr(settings, "OAUTH2_USER_CLASS")

        self.server = subprocess.Popen(("python", "%s/test_server.py" % (
            dirname(__file__))))


    def tearDown(self):
        try:
            self.server.kill()
        except: pass


    # a custom authentication method *MUST* be provided in order to
    # get the email address
    @staticmethod
    def auth(request, provider, client):
        data = client.request("/me")

        return User.objects.get_or_create(username="test",
            email=data["email"], access_token=client.access_token,
            provider_key=provider.name,
            expires=data.get("expires", -1))[0]


    def test_authenticate(self):
        for p in settings.OAUTH2_PROVIDERS:
            response = self.client.get("/o/auth/%s" % p.name.lower(),
                HTTP_HOST="unittest")
            self.assertEquals(response.status_code, 302)


    def test_code(self):
        for p in settings.OAUTH2_PROVIDERS:
            response = self.client.get("/o/code/%s" % p.name.lower(),
                HTTP_HOST="unittest", follow=True)


    def test_logout(self):
        for p in settings.OAUTH2_PROVIDERS:
            response = self.client.get("/o/logout", follow=True)
            self.assertEquals(response.status_code, 200)


class CustomUser(django.contrib.auth.models.User):
    access_token = models.CharField(max_length=100)
    expires = models.FloatField()
    provider_key = models.CharField(max_length=100)


class TestCustomBackend(TestCase):
    def setUp(self):
        settings.OAUTH2_USER_CLASS = "django_sanction.tests.CustomUser"
        settings.OAUTH2_AUTH_FN = \
            "django_sanction.tests.TestCustomBackend.auth"
        settings.OAUTH2_GET_USER_FN = \
            "django_sanction.tests.TestCustomBackend.get_user"
        self.server = subprocess.Popen(("python", "%s/test_server.py" % (
            dirname(__file__))))


    def tearDown(self):
        try:
            self.server.kill()
        except: pass


    # a custom authentication method *MUST* be provided in order to
    # get the email address
    @staticmethod
    def auth(request, provider, client):
        data = client.request("/me")

        return CustomUser.objects.get_or_create(email=data["email"],
            access_token=client.access_token,
            provider_key=provider.name,
            expires=data.get("expires", -1))[0]


    @staticmethod
    def get_user(user_id):
        return CustomUser.objects.get(id=user_id)


    def test_code(self):
        for p in settings.OAUTH2_PROVIDERS:
            response = self.client.get("/o/code/%s" % p.name.lower(),
                HTTP_HOST="unittest", follow=True)

            url, status = response.redirect_chain[-1]
            self.assertEquals(status, 302)


    def test_user_class(self):
        backend = AuthenticationBackend()
        self.assertEquals(backend.user_class, CustomUser)


    def test_get_user_function(self):
        backend = AuthenticationBackend()
        self.assertEquals(backend._AuthenticationBackend__get_user_fn,
            TestCustomBackend.get_user)


    def test_auth_function(self):
        backend = AuthenticationBackend()
        self.assertEquals(backend._AuthenticationBackend__authenticate_fn,
            TestCustomBackend.auth)


class TestResourceMiddleware(TestCase):
    def test_process_request(self):
        mw = ResourceMiddleware()
        req = HttpRequest()
        req.user = User()

        # provider_key = "" here
        try:
            req = ResourceMiddleware().process_request(req)
            self.fail()
        except: pass

        req = HttpRequest()
        req.user = BaseUser()

        req = ResourceMiddleware().process_request(req)



call_command("syncdb", interactive=False)

