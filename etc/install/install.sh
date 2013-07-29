#!/bin/bash

# Script to set up a Django project on Vagrant.

# Installation settings
source /vagrant/.env
PGSQL_VERSION=9.1
PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/django/.virtualenvs/$PRJ_NAME


# Add a user 'django' with password 'django' to host the virtualenv
useradd -d /home/django -m -r -p `openssl passwd django` -s /bin/bash django
usermod -a -G vagrant django

# Need to fix locale so that Postgres creates databases in UTF-8
cp -p $PROJECT_DIR/etc/install/etc-bash.bashrc /etc/bash.bashrc
locale-gen en_GB.UTF-8
dpkg-reconfigure locales
export LANGUAGE=en_GB.UTF-8
export LANG=en_GB.UTF-8
export LC_ALL=en_GB.UTF-8

# Install essential packages from Apt, avoiding post install questions (truly non-interactive)
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get upgrade -y
# Python dev packages
apt-get install -y build-essential python python-dev python-setuptools python-pip
# Dependencies for image processing with PIL
apt-get install -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev
# Git (we'd rather avoid people keeping credentials for git commits in the repo, but sometimes we need it for pip requirements that aren't in PyPI)
apt-get install -y git

# Postgresql
if ! command -v psql; then
    apt-get install -y postgresql-$PGSQL_VERSION libpq-dev
    cp $PROJECT_DIR/etc/install/pg_hba.conf /etc/postgresql/$PGSQL_VERSION/main/
    /etc/init.d/postgresql reload
fi

# Virtualenv global setup
if ! command -v pip; then
    easy_install -U pip
fi
if [[ ! -f /usr/local/bin/virtualenv ]]; then
    easy_install virtualenv stevedore virtualenv-clone virtualenvwrapper
fi

# Bash environment global setup
cp -p $PROJECT_DIR/etc/install/bashrc /home/django/.bashrc
su - django -c "mkdir -p /home/django/.pip_download_cache"

# Postgresql setup for project
createuser -Upostgres -d -R -S $PRJ_USER
createdb -Upostgres -O$PRJ_USER $PRJ_DB

# Virtualenv setup for project
su - django -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    PIP_DOWNLOAD_CACHE=/home/django/.pip_download_cache $VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements/$PRJ_ENV.txt"

echo "workon $PRJ_NAME" >> /home/django/.bashrc

# Set execute permissions on manage.py, as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/website/manage.py

# Django project setup
su - django -c "source /usr/local/bin/virtualenvwrapper.sh && workon $PRJ_NAME && add2virtualenv /vagrant/website/"
su - django -c "source /usr/local/bin/virtualenvwrapper.sh && workon $PRJ_NAME && add2virtualenv /vagrant/"
su - django -c "source $VIRTUALENV_DIR/bin/activate && fab -f /vagrant/fabfile.py $PRJ_ENV plug_all"
su - django -c "source $VIRTUALENV_DIR/bin/activate && cd $PROJECT_DIR && python website/manage.py syncdb --all --noinput && python website/manage.py migrate --fake"
