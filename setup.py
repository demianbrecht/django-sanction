import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

requires = [
	"django",
	"sanction",
]

setup(
	name="django_sanction_auth",
	keywords="python,oauth2,sanction,django",
	version="0.1.0",
	description="A Django front end for the sanction OAuth2 client library",
	author="Demian Brecht",
	author_email="demianbrecht@gmail.com",
	url="https://github.com/demianbrecht/django_sanction",
	install_requires=requires,
	long_description=README,
    classifiers=[
		"Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory"
    ],
	packages=["django_sanction",],
)
