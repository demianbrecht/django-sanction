# vim: ts=4 sw=4 et:
from json import loads
import time

from django_sanction.models import User

from example.util import parse_url, gunzip

# an authenticate method must be custom to the application in order
# to provider per-provider user data
def authenticate(request, provider, client):
    user_data = lookup_map[provider.name.lower()](client)
    user = User.objects.get_or_create(
        username=None, # we'll want the user to set this somewhere in the app
        provider_id=user_data["id"],
        email=user_data["email"],
        provider_key=provider.name)[0]

    key = provider.name.lower()
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


def get_google_user(client):
    data = client.request("/userinfo")
    return {
        "id": data["id"],
        "email": data["email"],
    }


def get_facebook_user(client):
    data = client.request("/me")
    return {
        "id": data["id"],
        "email": data["email"]
    }


def get_github_user(client):
    return {
        "id": client.request("/user")["id"],
        "email": client.request("/user/emails")[0],
    }


def get_stackexchange_user(client):
    data = client.request("/me", qs={
        "site": "stackoverflow.com",
        "key": "BbzA7ovVcI*4NtPJCc59CA((",
    }, parser=lambda d: loads(gunzip(d)))
    return {
        "id": data["items"][0]["user_id"],
        "email": None,
    }


data_map = {
    "google": get_google_data,
    "facebook": get_facebook_data,
    "github": get_github_data,
    "stackexchange": get_stackexchange_data,
}

lookup_map = {
    "google": get_google_user, 
    "facebook": get_facebook_user,
    "github": get_github_user,
    "stackexchange": get_stackexchange_user,
}

