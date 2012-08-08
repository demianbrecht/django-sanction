# vim: ts=4 sw=4 et:
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def anonymous_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        return fn(request, *args, **kwargs)
    return wrapper


def login_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.id:
            return HttpResponseRedirect(getattr(settings, "OAUTH2_LOGIN_URL",
                "/"))
        return fn(request, *args, **kwargs)
    return wrapper

