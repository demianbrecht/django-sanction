# vim: ts=4 sw=4 et:
from json import loads

from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django_sanction.util import get_def
from django_sanction.decorators import (
    anonymous_required,
    login_required,
)

from example.util import gunzip


class Home(TemplateView):
    template_name = "home.html"


    @method_decorator(anonymous_required)
    def dispatch(self, *args, **kwargs):
        return TemplateView.dispatch(self, *args, **kwargs)


    def get_context_data(self, **kwargs):
        return {
            "providers": settings.OAUTH2_PROVIDERS,
        }


class Profile(TemplateView):
    template_name = "profile.html"


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return TemplateView.dispatch(self, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        data = {}
        if hasattr(self, "get_%s" % self.request.user.provider_key):
            data = getattr(self, "get_%s" % self.request.user.provider_key)(
                self.request)

        return {
            "user": self.request.user,
            "data": data
        }


    def get_google(self, request):
        return request.user.resource.request("/userinfo")

    
    def get_facebook(self, request):
        return request.user.resource.request("/me")


    def get_github(self, request):
        return request.user.resource.request("/user")


    def get_stackexchange(self, request):
        return request.user.resource.request("/me", qs={
            "site": "stackoverflow.com",
            "key": "BbzA7ovVcI*4NtPJCc59CA((",
            }, parser=lambda d: loads(gunzip(d)))

