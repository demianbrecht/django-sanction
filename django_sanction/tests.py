# -*- coding: utf-8 -*- 
import sys
import unittest
from os.path import dirname
try:
    from urlparse import urlparse, parse_qsl
except ImportError: # pragma: no cover
    from urllib.parse import urlparse, parse_qsl

from django.conf import settings
try:
    # django < 1.6
    from django.conf.urls.defaults import patterns, include, url
except ImportError:
    from django.conf.urls import patterns, include, url

from django.http import HttpResponseForbidden
from sanction.client import Client as SanctionClient

# monkey-patch sanction.request_token for tests
def _request_token(self, **kwargs):
    if 'code' in kwargs:
        self.access_token = 'unit_test_token'
SanctionClient.request_token = _request_token

class TestViews(unittest.TestCase):
    def test_login(self):
        c = TestClient()
        provider_key = 'unit'
        resp = c.get('/o/login/{}/'.format(provider_key))

        self.assertEquals(resp.status_code, 302)
        rloc = urlparse(resp._headers['location'][1])
        sloc = urlparse(settings.SANCTION_PROVIDERS[provider_key][
            'auth_endpoint'])
        self.assertEquals(rloc.scheme, sloc.scheme)
        self.assertEquals(rloc.netloc, sloc.netloc)
        self.assertEquals(rloc.path, sloc.path)

    def test_invalid_csrf(self):
        c = TestClient()
        
        # no state param
        resp = c.get('/o/login/unit?code=foo')
        self.assertEquals(type(resp), HttpResponseForbidden)

        # invalid state param
        resp = c.get('/o/login/unit?code=foo&state=bar')
        self.assertEquals(type(resp), HttpResponseForbidden)

    def test_login_logout(self):
        c = TestClient()
        provider_key = 'unit'
        provider = settings.SANCTION_PROVIDERS[provider_key]

        # login redirect to provider
        resp = c.get('/o/login/{}/'.format(provider_key))
        rloc = urlparse(resp._headers['location'][1])
        query = dict(parse_qsl(rloc.query))
        self.assertTrue('state' in query)
        self.assertEquals('{}://{}{}'.format(rloc.scheme, rloc.netloc,
            rloc.path), provider['auth_endpoint'])

        # test login with code
        resp = c.get('/o/login/{}/?code=foo&state={}'.format(provider_key,
            query['state']))
        self.assertEquals(resp.status_code, 302)
        self.assertTrue('sessionid' in resp.cookies)

        # user's already logged in? should be redirected directly to their
        # profile
        resp = c.get('/o/login/{}/'.format(provider_key))
        self.assertEquals(resp.status_code, 302)
        rloc = urlparse(resp._headers['location'][1])
        self.assertEquals(rloc.path, settings.LOGIN_REDIRECT_URL)

        # test logout
        resp = c.get('/o/logout/')
        self.assertEquals(resp.status_code, 302)
        rloc = urlparse(resp._headers['location'][1])
        self.assertEquals(rloc.path, settings.LOGIN_URL)

if __name__ == '__main__':
    settings.configure(
        DEBUG = True,
        SECRET_KEY = 'UNIT_TEST',
        URL_CONF = 'django_sanction.tests',
        DATABASES = { 
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',                      
            }
        },
        AUTHENTICATION_BACKENDS = (
            'django_sanction.backends.AuthenticationBackend',
        ),
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles', 
            'django_sanction',
        ),
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies',
        ROOT_URLCONF = 'django_sanction.tests',
        LOGIN_URL = '/',
        LOGIN_REDIRECT_URL = '/profile',
        LOGOUT_URL = '/logout',
        SANCTION_PROVIDERS = { 
            'unit': { 
                'client_id': '421833888173.apps.googleusercontent.com',
                'client_secret': 'VueqKFZyz-aoL4rQFleEIT1j',
                'auth_endpoint': 'http://unit/oauth/dialog',
                'token_endpoint': 'http://unit/oauth/token',
                'resource_endpoint': 'http://unit/api',
                'redirect_uri': 'http://unit/login/unit',
                'scope': ('email',),
                },
            },
    )

    # the following stuff has to happen AFTER settings have been set
    sys.path.append(dirname(dirname(__file__)))
    from django.core.management import call_command
    from django.test.client import Client as TestClient

    from django.db import models

    class User(models.Model):
        class Meta:
            app_label = 'django_sanction'

        id = models.CharField(max_length=50, unique=True, primary_key=True)
        access_token = models.CharField(max_length=50, null=True)
        token_expires = models.FloatField(default=0)
        provider = models.CharField(max_length=25)
        last_login = models.DateTimeField(null=True)

        USERNAME_FIELD = 'id'
        REQUIRED_FIELDS = ['provider']

        def is_authenticated(self):
            return True

        @staticmethod
        def fetch_user(provider, access_token):
            user, new = User.objects.get_or_create(id='fb_foo')
            return user

        @staticmethod
        def get_user(user_id):
            return User.objects.get(id=user_id)
 
    setattr(settings, 'AUTH_USER_MODEL', 'django_sanction.User')

    call_command('syncdb', interactive=False)
    unittest.main()

urlpatterns = patterns('',
    url(r'^o/', include('django_sanction.urls')), 
)
