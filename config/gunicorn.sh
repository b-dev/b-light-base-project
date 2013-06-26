#!/bin/bash
set -e
LOGFILE=/home/django/%%nomesito%%/logs/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=django
GROUP=django
ADDRESS=127.0.0.1:8001
cd /home/django/%%nomesito%%/website
export DJANGO_ENVIRONMENT=production
source /home/django/.virtualenvs/%%nomesito%%/bin/activate
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS --bind=$ADDRESS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE --settings website.settings