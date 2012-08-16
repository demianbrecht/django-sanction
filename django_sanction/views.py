# vim: ts=4 sw=4 et:
from urllib import urlencode
from urlparse import (
    parse_qsl, 
    urlparse,
    urlunparse,
)
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.utils.crypto import (
    constant_time_compare,
)
from django.middleware.csrf import (
    CsrfViewMiddleware,
    get_token,
)

from sanction.client import Client


def auth_redirect(request, provider, client):
    kwargs = {}
    if "scope" in provider: kwargs["scope"] = provider["scope"]

    client.redirect_uri = _get_redirect_uri(request, provider)

    response = redirect(client.auth_uri(**kwargs))

    if getattr(settings, "OAUTH2_USE_CSRF", True):
        # inject the state query param
        CsrfViewMiddleware().process_view(request, response, [], {})
        url = list(urlparse(response["location"]))
        url_p = dict(parse_qsl(url[4]))
        url_p.update({"state": get_token(request)})
        url[4] = urlencode(url_p)
        response["location"] = urlunparse(url)

    return response


def auth_login(request, provider, client):
    if getattr(settings, "OAUTH2_USE_CSRF", True):
        if not request.GET.has_key("state") or \
            not constant_time_compare(get_token(request), request.GET["state"]):
            return HttpResponseForbidden()

    client.redirect_uri = _get_redirect_uri(request, provider)

    try:
        client.request_token(data=request.GET, parser=provider.get("parser",
            None), grant_type=provider.get("grant_type", None))
    except IOError as e:
        if hasattr(settings, "OAUTH2_EXCEPTION_URL"):
            url = "%s?%s" % (getattr(settings, "OAUTH2_EXCEPTION_URL"),
                urlencode({"error": e.message}))

            return HttpResponseRedirect("%s?%s" % (getattr(settings, "OAUTH2_EXCEPTION_URL"),
                urlencode({"error": e.message})))
        else:
            raise e

    user = authenticate(request=request, provider=provider,
        client=client)

    if user is not None:
        login(request, user)
    else:
        return HttpResponseForbidden()

    return redirect(settings.LOGIN_REDIRECT_URL)


def _get_redirect_uri(request, provider):
    return "%s://%s%s" % (_get_scheme(request), _get_host(request), 
        reverse_lazy(provider["code_view_name"]))


def _get_scheme(request):
    return getattr(settings, "OAUTH2_REDIRECT_URL_SCHEME",
        request.META.get("wsgi.url_scheme", "http"))


def _get_host(request):
    return getattr(settings, "OAUTH2_HOST", request.META["HTTP_HOST"])

