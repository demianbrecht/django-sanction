# vim: ts=4 sw=4 et:
import inspect

from django.conf import settings
from util import get_def


_SESSION_USER_ID_KEY = "user_id"

GRANT_TYPE_AUTHORIZATION_CODE = "code"
GRANT_TYPE_CLIENT_CREDENTIALS = "client_credentials"


class AuthenticationBackend(object):
    def __init__(self):
        if not hasattr(settings, "SANCTION_AUTH_FN"):
            raise KeyError("SANCTION_AUTH_FN must be in settings.py")

        if not hasattr(settings, "SANCTION_GET_USER_FN"):
            raise KeyError(
                "SANCTION_GET_USER_FN must be present in settings.py")


    @property
    def user_class(self):
        return self.__get_user_class()

    
    @property
    def __authenticate_fn(self):
        return self.__get_callable_def(settings, "SANCTION_AUTH_FN")


    @property
    def __get_user_fn(self):
        return self.__get_callable_def(settings, "SANCTION_GET_USER_FN")


    def __get_callable_def(self, obj, key):
        fn_name = getattr(obj, key)
        f = get_def(fn_name)
        assert(callable(f))
        return f


    def authenticate(self, request=None, provider=None, client=None):
        assert(request is not None)
        assert(provider is not None)
        assert(client is not None)

        return self.__authenticate_fn(request, provider, client)


    def get_user(self, user_id):
        return self.__get_user_fn(user_id)

    
   
    def __get_user_class(self):
        mod_name = getattr(settings, "SANCTION_USER_CLASS",
            "django.contrib.auth.models.User")
        c = get_def(mod_name)

        assert(inspect.isclass(c))
        return c



