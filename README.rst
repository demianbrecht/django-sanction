.. image:: https://secure.travis-ci.org/demianbrecht/django_sanction.png?branch=master 
   :target: http://travis-ci.org/#!/demianbrecht/django_sanction

WIP


TODOs
=====

Required
--------

* Create user profile class and store oauth-related data there
* Change example auth lookup to pull from the correct provider
* Inject sanction client into user object
* Custom login handling (auth_login in views.py)
* Custom error handling (i.e. redirect to login page vs 403)
* 100% unit test coverage
* Default CSRF protection


Nice to have
------------

* Testing a non-rel database
