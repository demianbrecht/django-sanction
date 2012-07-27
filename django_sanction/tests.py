# vim: ts=4 sw=4 et:

if __name__=="__main__":
    from BaseHTTPServer import (
        BaseHTTPRequestHandler,
        HTTPServer,
    )
    from json import dumps
    from urlparse import (
        parse_qsl,
        urlparse
    )

    class Handler(BaseHTTPRequestHandler):
        route_handlers = {
            "/oauth/dialog": "handle_dialog",
            "/oauth/token": "handle_token",
            "/oauth/api": "handle_api",
        }

        def do_POST(self):
            self.do_GET()

        def do_GET(self):
            url = urlparse(self.path)
            if url.path in self.route_handlers:
                getattr(self, self.route_handlers[url.path])(
                    dict(parse_qsl(url.query)))
            else:
                self.send_response(404)


        def success(func):
            def wrapper(self, *args, **kwargs):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.log_message(self.path)
                self.end_headers()
                return func(self, *args, **kwargs)
            return wrapper


        @success
        def handle_dialog(self, data):
            self.wfile.write(dumps({
                "error": "something_bad_happened"
            }))

        
        @success
        def handle_token(self, data):
            self.wfile.write(dumps({
                "access_token": "test_token"
            }))

        
        @success
        def handle_api(self, data):
            pass

    server_address = ("", 80)
    server = HTTPServer(server_address, Handler)
    server.serve_forever()
else:
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
            self.server = subprocess.Popen(("python", __file__,))


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

