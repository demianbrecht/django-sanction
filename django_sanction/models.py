# vim: ts=4 sw=4 et:
from django.db import models

from django.conf import settings
from django.contrib.auth.models import User as BaseUser

class User(BaseUser):
    provider_key = models.CharField(max_length=100)
    provider_id = models.CharField(max_length=256, blank=False)
    access_token = models.CharField(max_length=100)
    expires = models.FloatField(default=-1)

# TODO: Is this the best way of doing this??..
# nasty hack to allow email fields to be nullable
User._meta.fields[4].null = True

