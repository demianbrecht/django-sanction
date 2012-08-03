# vim: ts=4 sw=4 et:
from json import loads
import time

from django_sanction.models import User

from example.util import parse_url, unzip

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
    user.expires = data_map[key](client).get("expires", -1)
    user.save()

    return user


def get_google_data(client):
    return {
        "access_token": client.access_token,
        "expires": time.time() + float(client.expires_in),
    }


def get_github_data(client):
    return {
        "access_token": client.access_token,
    }


def get_facebook_data(client):
    return {
        "access_token": client.access_token,
        "expires": float(client.expires),
    }


def get_stackexchange_data(client):
    return {
        "access_token": client.access_token,
    }


def get_google_email(client):
    return client.request("/userinfo")["email"]


def get_facebook_email(client):
    return client.request("/me")["email"]


def get_github_email(client):
    return client.request("/user/emails")[0]


def get_stackexchange_email(client):
    import pdb; pdb.set_trace()
    r = client.request("/me", qs={
        "site": "stackoverflow.com",
        "key": "BbzA7ovVcI*4NtPJCc59CA((",
    }, parser=lambda d: loads(unzip(d)))
    return r


data_map = {
    "google": get_google_data,
    "facebook": get_facebook_data,
    "github": get_github_data,
    "stackexchange": get_stackexchange_data,
}

lookup_map = {
    "google": get_google_email, 
    "facebook": get_facebook_email,
    "github": get_github_email,
    "stackexchange": get_stackexchange_email,
}

