.PHONY: test example tags cloc lint

test:
	export PYTHONPATH=$$PYTHONPATH:`pwd` && python -m coverage run django_sanction/tests.py
	python -m coverage report -m


example:
	export PYTHONPATH=$$PYTHONPATH:`pwd` && \
	cd example && \
	python manage.py syncdb --noinput && \
	python manage.py runserver 8080


lint:
	pylint django_sanction --reports=n --include-ids=y


