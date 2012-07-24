# vim: ts=4 sw=4 et:
from django.conf import settings
from django.core.urlresolvers import reverse


class Provider(object):
    def __init__(self):
        name = self.__class__.__name__.upper()
        self.client_id = getattr(settings, "SANCTION_%s_CLIENT_ID" % name)
        self.secret_key = getattr(settings, "SANCTION_%s_CLIENT_SECRET" % name)
        self.scope = getattr(settings, "SANCTION_%s_SCOPE" % name, None)
        self.state = getattr(settings, "SANCTION_STATE", None)
        self.redirect_uri = getattr(settings, "SANCTION_%s_REDIRECT" % name,
            None)

        self.name = self.__class__.__name__
        self.view_name = "sanction-%s" % self.name.lower()


class Google(Provider):
    def __init__(self):
        Provider.__init__(self)
        self.auth_endpoint="https://accounts.google.com/o/oauth2/auth"
        self.token_endpoint="https://accounts.google.com/o/oauth2/token"
        self.resource_endpoint="https://www.googleapis.com/oauth2/v1"


class Facebook(Provider):
    def __init__(self):
        Provider.__init__(self)
        self.auth_endpoint="https://www.facebook.com/dialog/oauth"
        self.token_endpoint="https://graph.facebook.com/oauth/access_token"
        self.resource_endpoint="https://graph.facebook.com"

