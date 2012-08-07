# vim: ts=4 sw=4 et:

def anonymous_required(fn):
    def inner(*args, **kwargs):
        if args[0].user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        return fn(*args, **kwargs)
    return inner

