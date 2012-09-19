# vim: ts=4 sw=4 et:
""" Django authentication backend
"""
from django.conf import settings

from django_sanction.models import User
from django_sanction.util import get_def


class AuthenticationBackend(object):
    """ Django authentication backend implementation

    To install, add ``django_sanction.backends.AuthenticationBackend`` to
    your project's settings' ``AUTHENTICATION_BACKENDS``
    """
    def __init__(self):
        assert(hasattr(settings, 'OAUTH2_AUTH_FN'))

    # pylint: disable=R0201
    @property
    def user_class(self):
        """ The class used to define a user
        """
        return get_def(getattr(settings, 'OAUTH2_USER_CLASS',
            'django_sanction.models.User'))
    
    # pylint: disable=R0201 
    def authenticate(self, request=None, provider=None, client=None):
        """ Django API function, authenticating a user
        """
        return get_def(getattr(settings, 'OAUTH2_AUTH_FN'))(
            request, provider, client)

    def get_user(self, user_id):
        """ User lookup
        """
        try:
            return get_def(getattr(settings, 'OAUTH2_GET_USER_FN'))(
                user_id)
        except AttributeError:
            return User.objects.get(id=user_id)
