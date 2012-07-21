# vim: ts=4 sw=4 et:
import inspect

from django.conf import settings


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

    
    def authenticate(self, request=None, provider=None, grant_type=None):
        if grant_type is None: grant_type = GRANT_TYPE_AUTHORIZATION_CODE
        assert(request is not None)
        assert(provider is not None)

        if request and request.session.has_key("s_user") and \
            request.session.has_key("s_expires"):
            return self.__get_user_lookup_fn()(provider,
                request["s_user"])

        return None


    def get_user(self, user_id):
        return self.__get_user_lookup_fn()(user_id)

    
    def __get_user_lookup_fn(self):
        fn_name = getattr(settings, _AUTH_USER_LOOKUP_FN_KEY)
        f = self.__get_def(fn_name)

        assert(callable(f))
        return f


    def __get_user_class(self):
        mod_name = getattr(settings, _AUTH_USER_CLASS_KEY,
            "django.contrib.auth.models.User")
        c = self.__get_def(mod_name)

        assert(inspect.isclass(c))
        return c


    def __get_def(self, name):
        p = name.split(".")
        
        m = None
        for n in range(-1, -len(p), -1):
            mod = ".".join(p[:n])
            try:
                m = __import__(mod)
                if m is not None:
                    break
            except: pass
        assert(m is not None)

        for c in p[1:]:
            m = getattr(m, c)
        return m

