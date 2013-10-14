project_setup:
	pip install sh
	cd bin
	python bootstrap.py dev
	cd ../../
	add2virtualenv PRJ_NAME
	cd PRJ_NAME
	add2virtualenv website
	add2virtualenv external_apps
	pip install -r requirements/dev.txt
	python website/manage.py sycndb --all
	python website/manage.py migrate --fake