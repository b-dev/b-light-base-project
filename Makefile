install:
	pip install sh
	python bin/bootstrap.py $(ENV)
	fab $(ENV) setup
	python website/manage.py sycndb --all
	python website/manage.py migrate --fake