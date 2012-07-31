# vim: ts=4 sw=4 et:

class Provider(object):
    def __init__(self, name, client_id, client_secret, auth_endpoint, 
            token_endpoint, resource_endpoint, scope=None, state=None, 
            redirect_uri=None, parser=None):
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.state = state
        self.redirect_uri = redirect_uri
        self.parser = parser

        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.resource_endpoint = resource_endpoint
        
        self.auth_view_name = None
        self.code_view_name = None
        #view_name = self.name.lower()
        #self.auth_view_name = "sanction-%s-auth" % view_name 
        #self.code_view_name = "sanction-%s-code" % view_name 


