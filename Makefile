project_setup:
	pip install sh
	python bin/bootstrap.py dev
	pip install -r requirements/dev.txt
	python website/manage.py sycndb --all
	python website/manage.py migrate --fake