.. image:: https://secure.travis-ci.org/demianbrecht/django_sanction.png?branch=master 
   :target: http://travis-ci.org/#!/demianbrecht/django_sanction


.. contents::
   :depth: 3


Overview
========

``django_sanction`` is a Django wrapper for the sanction_ module, 
making OAuth2 authentication and resource requests as easy to implement 
as possible. The goals of the project are to be:

Provider agnostic
-----------------

There is no assumption made about what providers should be accounted for 
(as in the core sanction_ module). This means that while providers that 
follow the `OAuth2 spec`_ should be handled by default, deviant providers
may have to have custom implementations for certain handlers (see
stackexchange and facebook examples in the examples directory). This also
means that the user will need to have at least a basic understanding of
OAuth2 and provider implementations. However, the upside is that the library
is flexible in that library maintenance does not need to occur in order to
support new OAuth2 providers.


Persistence agnostic
--------------------

``django_sanction`` doesn't care if you use the provided 
``django_sanction.models.User`` model (which is an extension of the 
contrib.auth ``User`` model) or a custom nonrel user class, as long
as a few required attributes exist on the model:

* ``access_token``
  Resource access token granted by the OAuth2 provider
* ``expires``
  The token expiry date (if applicable, will be set to -1 if non-expiring)
* ``provider_id``
  The user ID as specified by the OAuth2 provider. This is a required
  field in the OAuth2 spec (while e-mail addresses are not).
* ``provider_key``
  The key (or name) or the provider used for a given user. This is used
  in order to look up the provider in the application's ``settings.py``
  file.


Flexible
--------

While most functionality is accounted for and provided out of the box,
``django_sanction`` is flexible where it makes sense to be. See the settings
section for more details.


Usage
=====

Required settings
-----------------

Define a list of providers in your settings.py file::

    OAUTH2_PROVIDERS = { 
        "google": { 
            "client_id": "421833888173.apps.googleusercontent.com",
            "client_secret": "VueqKFZyz-aoL4rQFleEIT1j",
            "auth_endpoint": "https://accounts.google.com/o/oauth2/auth",
            "token_endpoint": "https://accounts.google.com/o/oauth2/token",
            "resource_endpoint": "https://www.googleapis.com/oauth2/v1",
            "scope": ("email", "https://www.googleapis.com/auth/userinfo.profile",)
        },
        "facebook": {
            "client_id": "152107704926343",
            "client_secret": "80c81e4d7d5bc68ecc8cf1da0213382e",
            "auth_endpoint": "https://www.facebook.com/dialog/oauth",
            "token_endpoint": "https://graph.facebook.com/oauth/access_token",
            "resource_endpoint": "https://graph.facebook.com",
            "scope": ("email",),
            "parser": parse_url
        },
    }

As ``django_sanction`` and its parent module ``sanction`` are provider-
agnostic, you must supply the relevant data for each.

Required provider fields
````````````````````````

* ``client_id``

  The client id as provided by the resource provider

* ``client_secret``

  The client secret as provided by the resource provider

* ``auth_endpoint``

  The providers' auth dialog endpoint to which users will be redirected for authorization

* ``token_endpoint``

  The endpoint used to swap the grant code for an access token

* ``resource_endpoint``

  The endpoint used to access user resources

Optional provider fields
````````````````````````

* ``scope``
  
  A list of scope parameters to request extended permissions from a user

* ``redirect_uri``

  The registered URL that the user will be redirected back to upon authorization

* ``parser``

  The parser to use for returned provider data


:note: If a provider deviates from the OAuth 2.0 spec in how it returns user
       data, client code must provide a supporting parser. See Facebook and 
       StackExchange implementations in the example project.


Authentication
--------------

Implement an authentication routine (see the example project for implementation
details) and add it to your settings file::

    OAUTH2_AUTH_FN = "example.auth.authenticate"


Backend
-------

Add the authentication backend to your settings::

    AUTHENTICATION_BACKENDS = (
        "django_sanction.backends.AuthenticationBackend",
    )

``django_sanction`` will play nicely with authentication backends, so it's
perfectly valid to have multiple backends listed here.


Installed application
---------------------

Add ``django_sanction`` to your list of ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        # ...
        "django_sanction",
    )


URLs
----

Add this to your urls::

    urlpatterns = pattenrs("",
        # o/ can be sustituted for anything
        url(r'^o/", include(django_sanction.urls)),
    )

Resource middleware
-------------------

By using the ``ResourceMiddleware``, a fully usable ``sanction`` ``Client``
will be added to the current ``request.user``.

Add the middleware::

    MIDDLEWARE_CLASSES = (
        # ...
        "django_sanction.middleware.ResourceMiddleware"
    )

Access resources (i.e. Facebook) once a user has been authenticated::

    request.user.resource.request("/me")


Settings
========

* OAUTH2_PROVIDERS (**required**)

  The list of providers that are accessible to the application. See 
  ``settings.py`` in the example app for a sample implementation.

* OAUTH2_AUTH_FN (**required**)

  The function to use when authenticating a user. As ``django_sanction``
  doesn't know anything about the providers in use, it can't know how
  to construct a user with the provider's resources. As such, this must
  be provided by the user code.

* OAUTH2_EXCEPTION_URL (*suggested*)

  The URL to redirect the user to in the event of an OAuth2 exeption.
  An example of this may be if the user declines the authorization of
  your application. If this is not provided, ``django_sanction`` will simply
  redirect the user using ``HttpResponseForbidden()``

* OAUTH2_GET_USER_FN (*optional*)

  A function to look up the user. This will be required if using an
  alternate persistence mechanism than the one provided.

* OAUTH2_USER_CLASS (*optional*)
  The class to use for the user. This defaults to 
  ``django_sanction.models.User``.

* OAUTH2_REDIRECT_URL_SCHEME (*optional*)

  This should be supplied if the URL scheme (http or https) differs from
  the current request. This defaults to 
  ``request.META.get("wsgi.url_scheme", "http")``.

* OAUTH2_HOST (*optional*)
  
  Should be used if the HTTP host differs from the current request. This
  defaults to ``request.META["HTTP_HOST"]``.

.. _sanction: https://github.com/demianbrecht/sanction
.. _`oauth2 spec`: http://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&ved=0CGIQFjAA&url=http%3A%2F%2Ftools.ietf.org%2Fhtml%2Fietf-oauth-v2-30&ei=sBAtULqHDqPOiwK3zoDgDg&usg=AFQjCNGSdKvjocQl86fT8e-dp_53zeqR8g
