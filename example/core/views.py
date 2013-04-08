from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render_to_response('index.html')

@login_required
def profile(request):
    data = request.user._wrapped.__dict__
    provider = request.user.current_provider(request)
    data.update({
        'email': provider.email,
        'provider': provider.name,
        'pid': provider.pid,
    })

    return render_to_response('profile.html', data) 
