====================
D-light base project
====================

A complete skeleton for Django projects, currently using:
---------------------------------------------------------
* Django 1.5
* jquery 1.10
* jquery ui 1.10
* bootstrap 2.3

Project is configured to use Vagrant (1.2.2) on VirtualBox (4.2.12) during development,
tested with PyCharm on Ubuntu and MacOSX. ( note that currently VirtualBox 4.2.14 seems bugged and will fail when
importing the vagrant box )
Deployment is made with Gunicorn and Nginx.

================
Deployment
================

To deploy this application, you need to follow these steps:
-----------------------------------------------------------

Local deployment::
    git clone git@github.com:marcominutoli/b-light-base-project.git




If using Vagrant:
-----------------




If not using Vagrant:
---------------------

Create a virtualenv with::

    mkvirtualenv PROJECT_NAME

Bootstrap from the virtualenv::

    cd PROJECT_NAME/bin
    pip install sh
    python bootstrap.py PROJECT_NAME PROJECT_ENVIRONMENT


default for PROJECT_ENVIRONMENT is 'dev', other environment types are
---------------------------------------------------------------------

 * 'test' ( when deploying on a ci server )
 * 'staging'
 * 'production'


Add the external_apps and website directories to the virtualenv::

   cd ..
   add2virtualenv external_apps
   add2virtualenv website

Load the environment settings and run the script to configure the setup::

    deactivate
    workon PROJECT_NAME
    fab setup

Run syncdb and migrate::

   cd website
   ./manage.py syncdb --all
   ./manage.py migrate --fake





========================
django-twoscoops-project
========================

A project template for Django 1.5.

To use this project follow these steps:

#. Create your working environment
#. Download b-light-base-project from github
#. Create the new project using the django-two-scoops template
#. Install additional dependencies
#. Use the Django admin to create the project

*note: these instructions show creation of a project called "icecream".  You
should replace this name with the actual name of your project.*

Working Environment
===================

You have several options in setting up your working environment.  We recommend
using virtualenv to seperate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Virtualenv Only
---------------

First, make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv --distribute icecream

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

Virtualenv with virtualenvwrapper
--------------------------

In Linux and Mac OSX, you can install virtualenvwrapper (http://virtualenvwrapper.readthedocs.org/en/latest/),
which will take care of managing your virtual environments and adding the
project path to the `site-directory` for you::

    $ mkdir icecream
    $ mkvirtualenv -a icecream icecream-dev
    $ cd icecream && add2virtualenv `pwd`

Windows
----------

In Windows, or if you're not comfortable using the command line, you will need
to add a `.pth` file to the `site-packages` of your virtualenv. If you have
been following the book's example for the virtualenv directory (pg. 12), then
you will need to add a python pathfile named `_virtualenv_path_extensions.pth`
to the `site-packages`. If you have been following the book, then your
virtualenv folder will be something like::

`~/.virtualenvs/icecream/lib/python2.7/site-directory/`

In the pathfile, you will want to include the following code (from
virtualenvwrapper):

    import sys; sys.__plen = len(sys.path)
    /home/<youruser>/icecream/icecream/
    import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)

Download b-light-base-project from github
==========================================

Download b-light-base-project from github::

    $ git clone git@github.com:marcominutoli/b-light-base-project.git icecream

Creating your project
=====================

1. Enter in icecream directory::

    $ cd icecream

2. Install the project

    $ make install ENV=dev

Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*

Acknowledgements
================

    - Many thanks to Randall Degges for the inspiration to write the book and django-skel.
    - All of the contributors_ to this project.

.. _contributors: https://github.com/twoscoops/django-twoscoops-project/blob/master/CONTRIBUTORS.txt
