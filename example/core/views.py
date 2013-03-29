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
    data.update({
        'email': request.user.current_provider(request).email,
        'provider': request.user.current_provider(request).name,
    })
    api_map = {
        'google': '/userinfo',
        'facebook': '/me'
    }
    provider = request.user.current_provider(request)
    data['user_info'] = provider.resource.request(api_map[provider.name])
    return render_to_response('profile.html', data) 
