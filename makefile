.PHONY: test

test:
	nosetests -s --pdb --with-coverage --cover-package=django_sanction

