.PHONY: test

test:
	nosetests -s --with-coverage --cover-package=django_sanction

