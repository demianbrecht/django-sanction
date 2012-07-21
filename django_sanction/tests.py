# vim: ts=4 sw=4 et:
from django.conf import settings
settings.configure(
    SECRET_KEY = "UNIT_TEST",
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
    )
)

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import HttpRequest
from django.db import models
from django.test import TestCase
from django.test.client import Client

from django_sanction.backends import AuthenticationBackend
from django_sanction.providers import Google


class CustomUser(object):
    pass


def user_lookup(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return None


class TestBackend(TestCase):
    def setUp(self):
        self.cur_user = User.objects.create(username="test", email="test@test.com",
            password="foo")
        self.cur_user.save()


    @staticmethod
    def user_lookup(user_id):
        pass


    def test_init(self):
        # check failure with no user lookup
        try:
            be = AuthenticationBackend()
            self.fail("shouldn't hit here")
        except: pass

        settings.SANCTION_USER_LOOKUP_FN = \
            "django_sanction.tests.user_lookup"

        # check default user class
        be = AuthenticationBackend()
        self.assertEquals(be.user_class, User)

        # check custom user class
        settings.SANCTION_USER_CLASS = "django_sanction.tests.CustomUser"
        be = AuthenticationBackend()
        self.assertEquals(be.user_class, CustomUser)


    def test_unbound_lookup(self):
        # test simple def
        settings.SANCTION_USER_CLASS = "django_sanction.tests.CustomUser"
        settings.SANCTION_USER_LOOKUP_FN = \
            "django_sanction.tests.user_lookup"

        be = AuthenticationBackend()
        self.assertEquals(be.get_user(-1), None)


    def test_static_lookup(self):
        # test static method
        settings.SANCTION_USER_CLASS = "django_sanction.tests.CustomUser"
        settings.SANCTION_USER_LOOKUP_FN = \
            "django_sanction.tests.TestBackend.user_lookup"

        be = AuthenticationBackend()
        self.assertEquals(be.get_user(-1), None)


    def test_lookup_found(self):
        self.__init_settings()
        be = AuthenticationBackend()
        self.assertEquals(be.get_user(42), None)

        self.assertEquals(be.get_user(self.cur_user.id), self.cur_user)


    def test_login(self):
        c = Client()
        r = HttpRequest()
        r.session = {}
        self.assertIsNone(authenticate(request=r, provider=Google))

        r.session["s_user"] = "1"
        r.session["s_expires"] = 0
        self.assertIsNone(authenticate(request=r, provider=Google))


    def __init_settings(self):
        settings.SANCTION_USER_CLASS = "django.contrib.auth.models.User"
        settings.SANCTION_USER_LOOKUP_FN = \
            "django_sanction.tests.user_lookup"


call_command("syncdb", interactive=False)

