# vim: ts=4 sw=4 et:
import inspect

from django.conf import settings
from util import get_def


_SESSION_USER_ID_KEY = "user_id"

_AUTH_USER_LOOKUP_FN_KEY = "SANCTION_USER_LOOKUP_FN"
_AUTH_USER_CLASS_KEY = "SANCTION_USER_CLASS"


GRANT_TYPE_AUTHORIZATION_CODE = "code"
GRANT_TYPE_CLIENT_CREDENTIALS = "client_credentials"


class AuthenticationBackend(object):
    def __init__(self):
        if not hasattr(settings, _AUTH_USER_LOOKUP_FN_KEY):
            raise ValueError("%s must be specified in settings.py" % (
                _AUTH_USER_LOOKUP_FN_KEY))


    @property
    def user_class(self):
        return self.__get_user_class()

    
    def authenticate(self, request=None):
        """ The user should be redirected to [prefix]/auth/[provider] rather 
        than explicitly calling authenticate
        """
        raise NotImplementedError(
            "authenticate should not be used with the sanction backend")


    def get_user(self, user_id):
        return self.__get_user_lookup_fn()(user_id)

    
    def __get_user_lookup_fn(self):
        fn_name = getattr(settings, _AUTH_USER_LOOKUP_FN_KEY)
        f = get_def(fn_name)

        assert(callable(f))
        return f


    def __get_user_class(self):
        mod_name = getattr(settings, _AUTH_USER_CLASS_KEY,
            "django.contrib.auth.models.User")
        c = get_def(mod_name)

        assert(inspect.isclass(c))
        return c



