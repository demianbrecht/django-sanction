# vim: ts=4 sw=4 et:

class Provider(object):
    def __init__(self, auth_ep=None, token_ep=None, resource_ep=None):
        self.auth_ep = auth_ep
        self.token_ep = token_ep
        self.resource_ep = resource_ep


class Google(Provider):
    def __init__(self):
        Endpoint.__init__(self,
            auth_ep="https://accounts.google.com/o/oauth2/auth",
            token_ep="https://accounts.google.com/o/oauth2/token",
            resource_ep="https://www.googleapis.com/oauth2/v1")


class Facebook(Provider):
    def __init__(self):
        Endpoint.__init__(self,
            auth_ep="https://www.facebook.com/dialog/oauth",
            token_ep="https://graph.facebook.com/oauth/access_token",
            resource_ep="https://graph.facebook.com")

