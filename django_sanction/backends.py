# -*- coding: utf-8 -*- 
""" Django authentication backend
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from sanction import Client as SanctionClient

class AuthenticationBackend(object):
    """ Authentication backend for ``django_sanction``.

    The API defined here is required by Django.
    """
    def authenticate(self, code=None, provider_key=None):
        """ Django API function, authenticating a user

        Authentication method required of a Django authentication backend. If
        successful, this method will retrieve an access token from the
        provider.

        :note: A method ``fetch_user`` is expected as a static function on the
               custom user class. This is responsible for retrieiving the
               actual user instance required by the Django backend. It will
               receive the ``provider_key`` and an instance of a sanction
               client (which should contain the access token)

        :param code: The code returned by the OAuth 2.0 provider once the user
                     has given your application authorization.
        :param provider_key: The key for the provider sending authorization
                             data. This should match the keys used in your
                             settings file for ``SANCTION_PROVIDERS``.
        """
        model = get_user_model()
        provider = settings.SANCTION_PROVIDERS[provider_key]
        
        c = SanctionClient(token_endpoint=provider['token_endpoint'],
            resource_endpoint=provider['resource_endpoint'],
            auth_endpoint=provider['auth_endpoint'],
            client_id=provider['client_id'],
            client_secret=provider['client_secret'])

        c.request_token(code=code, parser=provider.get('parser', None),
                        redirect_uri=provider['redirect_uri'])

        return model.fetch_user(provider_key, c)

    def get_user(self, user_id):
        """ Gets the user given a user ID
        """
        return get_user_model().get_user(user_id)
