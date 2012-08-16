# vim: ts=4 sw=4 et:
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from sanction.client import Client

from django_sanction.models import User


class ResourceMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            try:
                provider = filter(lambda p: p["name"] == request.user.provider_key,
                    (settings.OAUTH2_PROVIDERS[k] for k in
                        settings.OAUTH2_PROVIDERS))[-1]

                c = Client(token_endpoint=provider["token_endpoint"],
                    resource_endpoint=provider["resource_endpoint"],
                    auth_endpoint=provider["auth_endpoint"],
                    redirect_uri=provider.get("redirect_uri", None),
                    client_id=provider["client_id"],
                    client_secret=provider["client_secret"])
                
                c.access_token = request.user.access_token
                c.expires = request.user.expires

                setattr(request.user, "resource", c)

            # play nice with other authentication backends
            except IndexError:
                raise KeyError("Provider %s doesn't exist" % 
                    request.user.provider_key)
            except AttributeError: 
                # current user isn't a django_sanction user
                pass

