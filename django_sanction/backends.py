# vim: ts=4 sw=4 et:
""" Django authentication backend
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from sanction.client import Client as SanctionClient

class AuthenticationBackend(object):
    # pylint: disable=R0201 
    def authenticate(self, code=None, provider_key=None):
        """ Django API function, authenticating a user

        The following attributes are expected to exist on the user instance:
        * ``id``
        * ``access_token``
        * ``provider``
        * ``token_expires``
        * ``get_user(provider, access_token)``
        """
        model = get_user_model()
        provider = settings.SANCTION_PROVIDERS[provider_key]
        
        c = SanctionClient(token_endpoint=provider['token_endpoint'],
            resource_endpoint=provider['resource_endpoint'],
            auth_endpoint=provider['auth_endpoint'],
            client_id=provider['client_id'],
            client_secret=provider['client_secret'],
            redirect_uri=provider['redirect_uri'])

        c.request_token(code=code, parser=provider.get('parser', None))

        return model.fetch_user(provider_key, c)

    def get_user(self, user_id):
        return get_user_model().get_user(user_id)
