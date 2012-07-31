# vim: ts=4 sw=4 et:
from django.conf import settings

from sanction.client import Client

class AuthMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            assert(request.user.provider_key in settings.SANCTION_PROVIDERS)

            provider = settings.SANCTION_PROVIDERS[request.user.provider_key]
            c = Client(token_endpoint=provider.token_endpoint,
                resource_endpoint=provider.resource_endpoint,
                auth_endpoint=provider.auth_endpoint,
                redirect_uri=provider.redirect_uri,
                client_id=provider.client_id,
                client_secret=provider.client_secret)
            
            c.access_token = request.user.access_token
            c.expires = request.user.expires

            setattr(request.user, "resource_endpoint", c)

