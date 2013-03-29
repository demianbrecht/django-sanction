from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, UserManager
from lazy import lazy
from sanction.client import Client as SanctionClient

class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 

    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=100, blank=True)
    last_name = models.CharField(_('last name'), max_length=100, blank=True)

    objects = UserManager()

    @lazy
    def providers(self):
        return dict((p.name, p) for p in Provider.objects.filter(user=self))

    
    def current_provider(self, request):
        return self.providers[request.session['p']]

    @staticmethod
    def fetch_user(provider, client):
        return getattr(User, 'fetch_{}'.format(provider))(client)

    @staticmethod
    def get_user(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def fetch_google(client):
        resp = client.request('/userinfo')
        normalized = {
            'id': resp['id'],
            'provider': 'google',
            'email': resp['email'],
            'first_name': resp['given_name'],
            'last_name': resp['family_name'],
            'access_token': client.access_token,
            'token_expires': client.token_expires,
        }
        return User._get(normalized)

    @staticmethod
    def fetch_facebook(client):
        resp = client.request('/me')
        normalized = {
            'id': resp['id'],
            'provider': 'facebook',
            'email': resp['email'],
            'first_name': resp['first_name'],
            'last_name': resp['last_name'],
            'access_token': client.access_token,
            'token_expires': (datetime.utcnow() - datetime(
                1970, 1, 1)).total_seconds(),
        }
        return User._get(normalized)

    @staticmethod
    def _get(data):
        try:
            provider = Provider.objects.get(name=data['provider'],
                pid=data['id'])
        except Provider.DoesNotExist:
            # TODO: do something unique with username
            user = User.objects.create(username='{}_{}'.format(
                data['provider'], data['id']),
                first_name=data['first_name'],
                last_name=data['last_name'])
            user.save()

            provider = Provider()
            provider.name = data['provider']
            provider.user = user
            provider.pid = data['id']
            provider.email = data['email']
            provider.access_token = data['access_token']
            provider.token_expires = data['token_expires']
            provider.save()

        return provider.user

class Provider(models.Model):
    name = models.CharField(_('provider'), max_length=50)
    user = models.ForeignKey(User)
    email = models.EmailField(_('email address'), blank=True)
    pid = models.CharField(_('provider id'), max_length=50)
    access_token = models.CharField(_('access token'), max_length=100,
        blank=True)
    token_expires = models.FloatField(default=0)

    @lazy
    def resource(self):
        provider = settings.SANCTION_PROVIDERS[self.name]
        c = SanctionClient(auth_endpoint=provider['auth_endpoint'],
            token_endpoint=provider['token_endpoint'],
            resource_endpoint=provider['resource_endpoint'],
            client_id=provider['client_id'],
            client_secret=provider['client_secret'])

        c.access_token = self.access_token
        return c
