# vim: ts=4 sw=4 et:
from django.conf import settings
from django.conf.urls import patterns, include, url

from util import get_def
from views import (
    auth_login,
    auth_redirect,
)

from sanction.client import Client

urlpatterns = patterns("") 

def append_auth_uri(key, provider, client):
    global urlpatterns
    urlpatterns += patterns("",
        url(r"^auth/%s" % key,
            lambda r: auth_redirect(r, provider, client),
            name=provider.auth_view_name))


def append_code_uri(key, provider, client):
    global urlpatterns
    urlpatterns += patterns("",
        url(r"^code/%s" % key, lambda r: auth_login(r, provider, client), 
            name=provider.code_view_name))
    

providers = getattr(settings, "SANCTION_PROVIDERS")
for key in providers:
    p = providers[key] 
    c = Client(auth_endpoint = p.auth_endpoint,
        token_endpoint = p.token_endpoint,
        resource_endpoint = p.resource_endpoint,
        client_id = p.client_id,
        client_secret = p.client_secret)

    name = key.lower()
    p.auth_view_name = "sanction-%s-auth" % name 
    p.code_view_name = "sanction-%s-code" % name 

    append_code_uri(key.lower(), p, c)
    append_auth_uri(key.lower(), p, c)

