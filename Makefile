project_setup:
	pip install sh
	python bin/bootstrap.py dev
	pip install -r requirements/base.txt
	python manage.py syncdb --all
	python manage.py migrate --fake