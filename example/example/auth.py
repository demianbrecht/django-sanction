# vim: ts=4 sw=4 et:
import time
from django_sanction.models import User

# an authenticate method must be custom to the application in order
# to provider per-provider user data
def authenticate(request, provider, client):
    email = lookup_map[provider.name.lower()](client)
    user = User.objects.get_or_create(
        username="%s_%s" % (provider.name.lower(), email,),
        email=email,
        provider_key=provider.name)[0]

    key = provider.name.lower()
    data_map[key](client)
    user.access_token = data_map[key](client)["access_token"]
    user.expires = data_map[key](client)["expires"]
    user.save()

    return user


def get_google_data(client):
    return {
        "access_token": client.access_token,
        "expires": time.time() + float(client.expires_in),
    }


def get_facebook_data(client):
    return {
        "access_token": client.access_token,
        "expires": float(client.expires),
    }


def get_google_email(client):
    return client.request("/userinfo")["email"]


def get_facebook_email(client):
    return client.request("/me")["email"]

data_map = {
    "google": get_google_data,
    "facebook": get_facebook_data,
}

lookup_map = {
    "google": get_google_email, 
    "facebook": get_facebook_email,
}

