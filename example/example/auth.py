from django.contrib.auth.models import User

def get_user(user_id):
	return User.objects.get(id=user_id)


def authenticate(request, provider, client):
	return User.objects.get_or_create(
		email=lookup_map[provider.name.lower()](client))[0]


def get_google_email(client):
	return client.request("/userinfo")["email"]


def get_facebook_email(client):
	return client.request("/me")["email"]


lookup_map = {
	"google": get_google_email, 
	"facebook": get_facebook_email,
}

