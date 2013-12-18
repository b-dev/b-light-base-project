project_setup:
	pip install sh
	python bin/bootstrap.py dev
	pip install -r requirements/base.txt
	python website/manage.py syncdb --all
	python website/manage.py migrate --fake