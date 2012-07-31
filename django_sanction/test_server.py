# vim: ts=4 sw=4 et:
from BaseHTTPServer import (
    BaseHTTPRequestHandler,
    HTTPServer,
)
from json import dumps
import time
from urlparse import (
    parse_qsl,
    urlparse
)


if __name__=="__main__":
    class Handler(BaseHTTPRequestHandler):
        route_handlers = {
            "/oauth/dialog": "handle_dialog",
            "/oauth/token": "handle_token",
            "/api": "handle_api",
            "/api/me": "handle_me", 
        }

        def do_POST(self):
            self.do_GET()

        def do_GET(self):
            url = urlparse(self.path)
            if url.path in self.route_handlers:
                getattr(self, self.route_handlers[url.path])(
                    dict(parse_qsl(url.query)))
            else:
                self.send_response(404)


        def success(func):
            def wrapper(self, *args, **kwargs):
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.log_message(self.path)
                self.end_headers()
                return func(self, *args, **kwargs)
            return wrapper


        @success
        def handle_dialog(self, data):
            self.wfile.write(dumps({
                "error": "something_bad_happened"
            }))

        
        @success
        def handle_token(self, data):
            self.wfile.write(dumps({
                "access_token": "test_token"
            }))


        @success
        def handle_me(self, data):
            self.wfile.write(dumps({
                "email": "unit@test.com",
                "expires": time.time()
            }))

        
        @success
        def handle_api(self, data):
            pass


    server_address = ("", 80)
    server = HTTPServer(server_address, Handler)
    server.serve_forever()

