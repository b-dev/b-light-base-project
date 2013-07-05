import os, time, random
from os.path import abspath, dirname

from fabric.api import *
from fabric.contrib.files import append, exists
from fabtools import require
import fabtools

SITE_ROOT = dirname(abspath(__file__))
GIT_REPO = 'GIT_REPO'

from _set_local_env_vars import import_env_vars
import_env_vars(SITE_ROOT)

PRJ_ENV = os.environ['PRJ_ENV']
PRJ_NAME = os.environ['PRJ_NAME']
PRJ_DB = os.environ['PRJ_DB']
PRJ_USER = os.environ['PRJ_USER']
PRJ_PASS = os.environ['PRJ_PASS']


ENVIRONMENTS = {
    'dev': ['127.0.0.1'],
    'staging': ['placehold-staging'],
    'production': ['placehold-production'],
    'test': ['placehold-test'],
}

env.user = 'django'

# sshagent_run credits to http://lincolnloop.com/blog/2009/sep/22/easy-fabric-deployment-part-1-gitmercurial-and-ssh/
# modified by dvd :)
def sshagent_run(cmd, capture=True):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """

    cwd = env.get('cwd', '')
    if cwd:
        cmd = 'cd %s;%s' % (cwd, cmd)

    with settings(cwd=''):
        for h in env.hosts:
            try:
                # catch the port number to pass to ssh
                host, port = h.split(':')
                local('ssh -p %s -A %s@%s "%s"' % (port, env.user, host, cmd), capture=capture)
            except ValueError:
                local('ssh -A %s@%s "%s"' % (env.user, h, cmd), capture=capture)

@task
def dev():
    env.name = 'dev'
    env.hosts = ENVIRONMENTS[env.name]

@task
def staging():
    env.name = 'staging'
    env.hosts = ENVIRONMENTS[env.name]

@task
def production():
    env.name = 'production'
    env.hosts = ENVIRONMENTS[env.name]

@task
def test():
    env.name = 'production'
    env.hosts = ENVIRONMENTS[env.name]

@task
def configure_db():
    if env.name == 'dev':
        from sh import createuser, createdb
        #todo untested
        createuser("-Upostgres -d -R -S %s" % PRJ_USER)
        createdb ("-Upostgres -O%s %s" % PRJ_USER, PRJ_DB)
    else:
        require.postgres.server()
        require.postgres.user(PRJ_USER, PRJ_PASS)
        require.postgres.database(PRJ_DB, PRJ_USER)

@task
def configure_git():
    from sh import rm
    rm('.hgignore', '-f')
    rm('.hg', '-f', '-r')
    rm('.git', '-f', '-r')
    git_username = raw_input(u"username on bitbucket ? \n")
    fabtools.require.git.command()
    local('git init')
    local('git remote add origin ssh://git@bitbucket.org/%s/%s.git' % (git_username, PRJ_NAME.lower()))
    local('git add .')
    local('git commit -m "First commit"')
    local('git push -u origin master')

@task
def setup():
    configure_db()

@task
def add_webapp():
    from sh import pip
    for line in pip.install('-r%s/requirements/webapp.txt' % SITE_ROOT, _iter=True):
        print line

    pah = os.path.join(SITE_ROOT, '.env')
    with open(pah, 'r+') as envfile:
        lines = envfile.readlines()
        for line in lines: pass #todo "search and replace or append" instead of just appending
        envfile.writelines(['export PRJ_IS_WEBAPP=TRUE', ])


@task
def project_setup():
    if not exists("/home/django/.virtualenvs/%s" % PRJ_NAME):
        run('mkvirtualenv %s' % (PRJ_NAME,))

    # Clono, se non e' gia stato clonato il progetto
    with cd("/home/django/"):
        if not exists(PRJ_NAME):
            sshagent_run('git clone %s %s' % (GIT_REPO, PRJ_NAME))

        with prefix('workon %s' % PRJ_NAME):
            # Aggiungo all'ambiente virtuale la directory base del progetto e la directory apps
            run("add2virtualenv /home/django/%s" % PRJ_NAME)
            run("add2virtualenv /home/django/%s/external_apps" % PRJ_NAME)
            run("add2virtualenv /home/django/%s/website" % PRJ_NAME)

            with cd(PRJ_NAME):
                # Installo i pacchetti necessari
                run("pip install -r requirements/%s.txt" % env.name)
                #if ENABLE_CMS:
                #    run("pip install -r requirements/cms.txt")

    # Installo dlight e altre applicazioni necessarie
    #with cd("/home/django/%s/apps" % PRJ_NAME):
    #    sshagent_run('hg clone ssh://hg@bitbucket.org/marcominutoli/dlight')
    #    sshagent_run('git clone https://github.com/marcominutoli/django-oscar.git')
    #    run("ln -s django-oscar/oscar oscar")

    # Creo un file local.py in settings per la gestione del db
    db_user = prompt("Nome utente postgres:")
    db_pwd = prompt("Digitare una password per l'utente %s:" % db_user)

    # Creo un file local.py in settings per la gestione del db
    db_name = prompt("Nome database da creare:")
    run("createdb -U %s -h localhost %s" % (db_user, db_name))

    with cd("/home/django/%s/" % PRJ_NAME):
        run("touch .env")
        append(".env", "PRJ_ENV=production")
        append(".env", "PRJ_ENGINE=postgresql_psycopg2")
        append(".env", "PRJ_NAME=%s" % PRJ_NAME)
        append(".env", "PRJ_DB=%s" % db_name)
        append(".env", "PRJ_USER=%s" % db_user)
        append(".env", "PRJ_PASS=%s" % db_pwd)
        append(".env", 'PRJ_SECRET_KEY="%s"' % "".join([random.choice(
                             "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_+)") for i in range(50)]))

    # Installazione app e db
    with cd("/home/django/%s/website" % PRJ_NAME):
        with prefix('workon %s' % PRJ_NAME):
            run("python manage.py syncdb --all")
            run("python manage.py migrate --fake")
            run("python manage.py collectstatic")

    env.user = 'root'

    # Per sicurezza, rendo eseguibile il file conf/gunicorn.sh
    with cd("/home/django/%s/config" % PRJ_NAME):
        run("chmod +x gunicorn.sh")

    with cd("/etc/nginx/sites-enabled/"):
        run("ln -s /home/django/%s/config/nginx.conf %s" % (PRJ_NAME, PRJ_NAME))

    with cd("/etc/supervisor/conf.d/"):
        run("ln -s /home/django/%s/config/supervisor.conf %s.conf" % (PRJ_NAME, PRJ_NAME))

    run("/etc/init.d/supervisor stop")
    time.sleep(5)
    run("/etc/init.d/supervisor start")
    run("supervisorctl reload")
    run("/etc/init.d/nginx reload")


@task
def update():
    # Clono, se non e' gia stato clonato il progetto
    with cd("/home/django/%s" % PRJ_NAME):
        sshagent_run("git pull")
        with prefix('workon %s' % PRJ_NAME):
            run("pip install -r requirements/%s.txt" % env.name)
            run("python website/manage.py migrate")
            run("python website/manage.py collectstatic --noinput")

    env.user = 'root'
    run('supervisorctl reload')


@task
def reload_server():
    env.user = 'root'
    run('/etc/init.d/nginx reload')
    run('supervisorctl reload')


@task
def restart_server():
    env.user = 'root'
    run('/etc/init.d/nginx restart')
    run("/etc/init.d/supervisor stop")
    time.sleep(5)
    run("/etc/init.d/supervisor start")
