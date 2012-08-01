.PHONY: test example

test:
	nosetests -s --pdb --with-coverage --cover-package=django_sanction


example:
	cd example; \
	rm sql.db; \
	python manage.py syncdb; \
	python manage.py runserver 80

