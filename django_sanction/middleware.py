# vim: ts=4 sw=4 et:
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from sanction.client import Client


class ResourceMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            provider = filter(lambda p: p.name == request.user.provider_key,
                settings.OAUTH2_PROVIDERS)[-1]

            if provider is None:
                raise KeyError("Provider %s doesn't exist" % 
                    request.user.provider_key)

            c = Client(token_endpoint=provider.token_endpoint,
                resource_endpoint=provider.resource_endpoint,
                auth_endpoint=provider.auth_endpoint,
                redirect_uri=provider.redirect_uri,
                client_id=provider.client_id,
                client_secret=provider.client_secret)
            
            c.access_token = request.user.access_token
            c.expires = request.user.expires

            setattr(request.user, "resource", c)

