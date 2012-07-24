# vim: ts=4 sw=4 et:
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

from util import get_def

from sanction.client import Client

urlpatterns = patterns("") 

def append_auth_uri(provider, client):
    kwargs = {}
    if provider.scope is not None: kwargs["scope"] = provider.scope
    if provider.state is not None: kwargs["state"] = provider.state
    if provider.redirect_uri is not None: kwargs[
        "redirect_uri"] = provider.redirect_uri

    global urlpatterns
    name = provider.name.lower()
    urlpatterns += patterns("",
        url(r"^auth/%s" % name,
            lambda r: redirect(client.auth_uri(**kwargs)),
            name=provider.auth_view_name))


def auth_login(request=None):
    login(request, authenticate(request=request))
    redirect(settings.LOGIN_REDIRECT_URL)
    

def append_code_uri(provider, client):
    global urlpatterns
    name = provider.name.lower()
    urlpatterns += patterns("",
        url(r"^code/%s" % name, auth_login, name=provider.code_view_name))
    

for provider in getattr(settings, "SANCTION_PROVIDERS"):
    p = get_def(provider)()
    c = Client(auth_endpoint = p.auth_endpoint,
        client_id = p.client_id)

    append_auth_uri(p, c)
    append_code_uri(p, c)

