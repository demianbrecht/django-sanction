# -*- coding: utf-8 -*- 
import logging

try: # pragma: no cover
    from urllib import urlencode
    from urlparse import parse_qsl, urlparse, urlunparse
except ImportError: # pragma: no cover
    from urllib.parse import urlencode, parse_qsl, urlparse, urlunparse

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect

from django.conf import settings
from django.contrib.auth import login as django_login, authenticate
from django.core.exceptions import PermissionDenied 
from django.utils.crypto import constant_time_compare
from django.middleware import csrf
from django.middleware.csrf import CsrfViewMiddleware

from sanction import Client as SanctionClient

def login(request, provider):
    """ Log in the current user following the OAuth 2.0 server flow

    This will follow one of two paths depending on the state of the request:

    **Initial entry**

    Initial entry state simply means that the user has not yet visited the
    provider to grant (or deny) authorization. In this state, a correct URL
    will be generated (provider-specific based on settings in
    ``SANCTION_PROVIDERS``) and the user will be redirected.

    **Token exchange**
    
    In this state, the user has already visited the providers' authorization
    page and has accepted the authorization request. The provider has returned
    the user to the login page, providing an OAuth 2.0 "code". This code is
    exchanged for an access token and the user is redirected to 
    ``LOGIN_REDIRECT_URL`` after they have been logged in.
    """
    if not isinstance(request.user, AnonymousUser):
        return redirect(settings.LOGIN_REDIRECT_URL)

    if 'code' not in request.GET:
        return _redirect(request, provider)
    else:
        return _login(request, provider)

def _redirect(request, provider):
    p = settings.SANCTION_PROVIDERS[provider]
    c = SanctionClient(auth_endpoint=p['auth_endpoint'],
        client_id=p['client_id'], token_endpoint=p['token_endpoint'],
        client_secret=p['client_secret'], 
        resource_endpoint=p['resource_endpoint'])

    kwargs = p.get('auth_params', {})
    response = redirect(c.auth_uri(redirect_uri = p['redirect_uri'],
                                   scope = p['scope'] if 'scope' in p else None, 
                                   **kwargs))

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
        if not 'state' in request.GET:
            logging.error(
                'SANCTION_USE_CSRF=True but "state" not defined in GET')
            raise PermissionDenied

        if not constant_time_compare(csrf.get_token(request), request.GET[
            'state']):
            logging.error('state GET param does not match session state')
            raise PermissionDenied

    user = authenticate(code=request.GET['code'], provider_key=provider)

    if user is not None:
        request.session['__sp'] = provider 
        django_login(request, user)
    else: # pragma: no cover
        logging.error('Unable to authenticate user')
        raise PermissionDenied

    return redirect(settings.LOGIN_REDIRECT_URL)
