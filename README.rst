====================
D-light base project
====================

A complete skeleton for Django projects, using:
-----------------------------------------------
* Django 1.5
* Pip in virtualenv(wrapper)
* Bower

Project is configured to use Vagrant (1.2.2) on VirtualBox (4.2.12) during development, tested with PyCharm on Ubuntu and MacOSX.
Deployment is made with Gunicorn and Nginx.


================
Deployment
================

To deploy this application, you need to follow these steps:
-----------------------------------------------------------

Local deployment::

    git clone git@github.com:marcominutoli/b-light-base-project.git [project_name]
    cd [project_name]

default for the project environment is 'dev', environment types are:

 * 'dev' ( the usual stuff; embedded static files serving, debug toolbar, django extensions )
 * 'test' ( todo description )
 * 'staging' ( todo description )
 * 'production' ( todo description )

'pluggable apps groups' are sets of deploy actions on the vagrant machine and python apps installed as part of the base project.
currently the groups are:

 * 'webapp' : installs redis server and configures in the django project django-rest-framework


If not using Vagrant:
---------------------

mkvirtualenv [project_name] && add2virtualenv . && add2virtualenv website && add2virtualenv external_apps
make project_setup


If using Vagrant:
-----------------

( note that currently VirtualBox 4.2.14 seems bugged and will fail when importing the vagrant box )::
    vagrant plugin install vagrant-vbguest  ( just the first time )
    cd ..
    vagrant up

This initialize a virtual machine with a user 'django' (password 'django') providing a virtualenv connected to the project.
Debian packages are kept upgraded by the provisioning as long PRJ_DEB_UPGRADE=TRUE in .env file.
The same for Pip packages in the virtualenv with PRJ_PIP_UPGRADE=TRUE.


When deploying:
---------------

TODO

Making your own pluggable app group
-----------------------------------

TODO

================
Acknowledgements
================

    - https://github.com/twoscoops/django-twoscoops-project
    - https://github.com/torchbox/vagrant-django-template
    - todo
