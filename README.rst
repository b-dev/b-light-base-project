====================
D-light base project
====================

A complete skeleton for Django projects, using:
-----------------------------------------------
* Django 1.6
* Pip in virtualenv(wrapper)
* Bower

Project also have a configuration to use Vagrant (1.2.2) on VirtualBox (4.2.12) during development, tested with PyCharm on Ubuntu and MacOSX.
Deployment is made with Gunicorn and Nginx.


==================================
Local Development without Vagrant
==================================

To locally deploy this template into a new project, you need to follow these steps:
-----------------------------------------------------------------------------------

::

    git clone git@github.com:marcominutoli/b-light-base-project.git [project_name]

::

    cd [project_name]
    mkvirtualenv [project_name]
    make project_setup


Add external (included) apps to the project
-------------------------------------------

There are two 'pre-installed' apps inside the base project: the CMS apps and the WEBAPP apps.
The CMS apps enable 'django-cms' apps and the relative settings.
The WEBAPP enable the 'django-rest-framework' apps, so you can easly expose your api to the web.

To enable these apps run the following command:

::

    fab plug cms # for the CMS apps
    fab plug webapp # for the WEBAPP apps


==================================
Local Development with Vagrant
==================================

To locally deploy this template into a new project with Vagrant, you need to follow these steps:
------------------------------------------------------------------------------------------------

::

    git clone git@github.com:marcominutoli/b-light-base-project.git [project_name]

::

    cd [project_name]/bin
    python bootstrap.py [env_type]

env_type choices are:

 * 'dev' ( the usual stuff; embedded static files serving, debug toolbar, django extensions )
 * 'test' ( todo description )
 * 'staging' ( todo description )
 * 'production' ( todo description )

( note that currently VirtualBox 4.2.14 seems bugged and will fail when importing the vagrant box )::
::

    vagrant plugin install vagrant-vbguest  ( just the first time )
    cd ..
    vagrant up

This initialize a virtual machine with a user 'django' (password 'django') providing a virtualenv connected to the project.
Debian packages are kept upgraded by the provisioning as long PRJ_DEB_UPGRADE=TRUE in .env file.
The same for Pip packages in the virtualenv with PRJ_PIP_UPGRADE=TRUE.

The vagrant-vbguest plugin will keep VirtualBox Guest Additions up to date on the VM,
if the base vagrant image has already additions installed an error could be thrown, in that case you should vagrant ssh and :
::

    sudo apt-get remove virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11
    sudo dpkg --purge virtualbox-guest-utils virtualbox-guest-x11
    sudo apt-get autoremove
    exit
    vagrant reload --provision


When deploying:
---------------

TODO

Adding a pluggable app group
-----------------------------------

'pluggable apps groups' are sets of deploy actions on the vagrant machine and python apps installed as part of the base project.
currently the groups are:

 * 'webapp' : installs redis server and configures in the django project django-rest-framework


================
Acknowledgements
================

    - https://github.com/twoscoops/django-twoscoops-project
    - https://github.com/torchbox/vagrant-django-template
    - https://zapier.com/engineering/profiling-python-boss/
