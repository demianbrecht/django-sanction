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



Settings
========

* OAUTH2_PROVIDERS (*required*)
  The list of providers that are accessible to the application. See 
  ``settings.py`` in the example app for a sample implementation.
* OAUTH2_AUTH_FN (*required*)
  The function to use when authenticating a user. As ``django_sanction``
  doesn't know anything about the providers in use, it can't know how
  to construct a user with the provider's resources. As such, this must
  be provided by the user code.
* OAUTH2_EXCEPTION_URL (*suggested*)
  The URL to redirect the user to in the event of an OAuth2 exeption.
  An example of this may be if the user declines the authorization of
  your application.
* OAUTH2_GET_USER_FN (**optional**)
  A function to look up the user. This will be required if using an
  alternate persistence mechanism than the one provided.
* OAUTH2_USER_CLASS (**optional**)
  The class to use for the user. This defaults to 
  ``django_sanction.models.User``.
* OAUTH2_REDIRECT_URL_SCHEME
  
* OAUTH2_HOST

