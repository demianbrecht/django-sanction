import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

requires = [
	"django",
	"sanction",
]

setup(
	name="django-sanction",
	keywords="python,oauth2,sanction,django",
	version="0.3.1",
	description="A Django front end for the sanction OAuth2 client library",
	author="Demian Brecht",
	author_email="demianbrecht@gmail.com",
	url="https://github.com/demianbrecht/django-sanction",
	install_requires=requires,
	long_description=README,
    classifiers=[
		"Development Status :: 4 - Beta",
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
	download_url='https://github.com/demianbrecht/django-sanction',
	platforms=None,
	license='MIT'
)
