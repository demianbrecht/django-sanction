# vim: ts=4 sw=4 et:
from json import loads
import time

from django_sanction.models import (
    User,
)

from example.util import parse_url, gunzip

# an authenticate method must be custom to the application in order
# to provide per-provider user data
def authenticate(request, provider, client):
    user_data = lookup_map[provider["name"].lower()](client)
    user, created = User.objects.get_or_create(
        provider_id=user_data["id"],
        provider_key=provider["name"])


    if created:
        # username should be either set by the user or 
        # by application logic
        user.username = "empty"
    user.email = user_data["email"]
    user.first_name = user_data.get("first_name", " ")
    user.last_name = user_data.get("last_name", " ")

    key = provider["name"].lower()
    normalized = normalize_attribs(client)
    user.access_token = normalized["access_token"]
    user.expires = normalized["expires"]
    user.save()

    return user


def _get_expires_time(client):
    try:
        key = filter(lambda attr: hasattr(client, attr), (
            "expires", "expires_in"))[-1]
        return time.time() + float(getattr(client, key))
    except IndexError:
        return -1
    


def normalize_attribs(client):
    return {
        "access_token": client.access_token,
        "expires": _get_expires_time(client), 
    }


def get_google_user(client):
    data = client.request("/userinfo")
    return {
        "id": data["id"],
        "email": data["email"],
        "first_name": data["given_name"],
        "last_name": data["family_name"],
    }


def get_facebook_user(client):
    data = client.request("/me")
    return {
        "id": data["id"],
        "email": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
    }


def get_github_user(client):
    return {
        "id": client.request("/user")["id"],
        "email": client.request("/user/emails")[0],
    }


def get_stackexchange_user(client):
    data = client.request("/me", query={
        "site": "stackoverflow.com",
        "key": "BbzA7ovVcI*4NtPJCc59CA((",
    }, parser=lambda d: loads(gunzip(d)))
    return {
        "id": data["items"][0]["user_id"],
        "email": None,
    }


lookup_map = {
    "google": get_google_user, 
    "facebook": get_facebook_user,
    "github": get_github_user,
    "stackexchange": get_stackexchange_user,
}

