# vim: ts=4 sw=4 et:
import logging

from urllib import urlencode
from urlparse import parse_qsl, urlparse, urlunparse
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect

from django.conf import settings
from django.contrib.auth import login as django_login, authenticate
from django.core.exceptions import PermissionDenied 
from django.utils.crypto import constant_time_compare
from django.middleware import csrf
from django.middleware.csrf import CsrfViewMiddleware

from sanction.client import Client as SanctionClient

def login(request, provider):
    if not isinstance(request.user, AnonymousUser):
        return redirect(settings.LOGIN_REDIRECT_URL)

    if 'code' not in request.GET:
        return _redirect(request, provider)
    else:
        return _login(request, provider)

def _redirect(request, provider):
    p = settings.SANCTION_PROVIDERS[provider]
    c = SanctionClient(auth_endpoint=p['auth_endpoint'],
        client_id=p['client_id'], redirect_uri=p['redirect_uri'])

    response = redirect(c.auth_uri(p['scope'] if 'scope' in p else None))

    # inject the state query param
    if getattr(settings, 'SANCTION_USE_CSRF', True):
        CsrfViewMiddleware().process_view(request, response, [], {})
        url = list(urlparse(response['location']))
        urlp = dict(parse_qsl(url[4]))
        urlp.update({'state': csrf.get_token(request)})
        url[4] = urlencode(urlp)
        response['location'] = urlunparse(url)

    return response

def _login(request, provider):
    if getattr(settings, 'SANCTION_USE_CSRF', True):
        if not request.GET.has_key('state'):
            logging.error(
                'SANCTION_USE_CSRF=True but "state" not defined in GET')
            raise PermissionDenied

        if not constant_time_compare(csrf.get_token(request), request.GET[
            'state']):
            logging.error('state GET param does not match session state')
            raise PermissionDenied

    user = authenticate(code=request.GET['code'], provider_key=provider)

    if user is not None:
        request.session['p'] = provider 
        django_login(request, user)
    else: # pragma: no cover
        logging.error('Unable to authenticate user')
        raise PermissionDenied

    return redirect(settings.LOGIN_REDIRECT_URL)
