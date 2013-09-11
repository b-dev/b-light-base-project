import os, time, random, getpass
from os.path import abspath, dirname, isfile

from fabric.api import *
from fabric.contrib.files import append, exists
from fabtools import require
import fabtools

SITE_ROOT = dirname(abspath(__file__))

from _set_local_env_vars import import_env_vars
import_env_vars(SITE_ROOT)

PRJ_ENV = os.environ['PRJ_ENV']
PRJ_NAME = os.environ['PRJ_NAME']
PRJ_DB = os.environ['PRJ_DB']
PRJ_USER = os.environ['PRJ_USER']
PRJ_PASS = os.environ['PRJ_PASS']

PRJ_GIT_REPO = os.environ['PRJ_GIT_REPO']
PRJ_ADDR_STAGING = os.environ['PRJ_ADDR_STAGING']
PRJ_ADDR_PRODUCTION = os.environ['PRJ_ADDR_PRODUCTION']
PRJ_ADDR_TEST = os.environ['PRJ_ADDR_TEST']

ENVIRONMENTS = {
    'dev': ['127.0.0.1'],
    'staging': PRJ_ADDR_STAGING,
    'production': PRJ_ADDR_PRODUCTION,
    'test': PRJ_ADDR_TEST,
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
def setup():
    configure_db()


@task
def bower():
    from sh import bower
    pah = os.path.join(SITE_ROOT, 'requirements', 'clientside.txt')
    with open(pah, 'r') as reqfile:
        for line in reqfile:
            bower.install(line.strip())

@task
def plug_prerequisites(name):
    env.user = 'vagrant'
    pah = os.path.join(SITE_ROOT, 'etc', 'install', 'plug_%s.pkg' % name)
    packages_to_install = []
    with open(pah, 'r') as pkgs_file:
        lines = pkgs_file.readlines()
        for line in lines:
            if len(line) and not line[0:1] == '#':
                packages_to_install.append(line.strip())
    require.deb.packages(packages_to_install)

@task
def plug_packages(name):
    from sh import pip
    for line in pip.install('-r%s/requirements/plug_%s.txt' % (SITE_ROOT, name), _iter=True):
        print line


def set_plug_active(name, pah=os.path.join(SITE_ROOT, '.env')):
    templines = []
    with open(pah, 'r') as envfile:
        lines = envfile.readlines()
        found = False
        for line in lines:
            if line.find('export PRJ_IS_%s=' % name.upper()) == 0:
                if line.find('TRUE') == 0:
                    templines.append(line)
                else:
                    templines.append(line.replace('FALSE', 'TRUE'))
                found = True
            else:
                templines.append(line)
        if not found:
            templines.append('\nexport PRJ_IS_%s=TRUE' % name.upper())
    with open(pah, 'w') as newfile:
        newfile.writelines(templines)

@task
def plug(name):
    set_plug_active(name)
    # replace_or_append('export PRJ_IS_%s=FALSE' % name.upper(), 'export PRJ_IS_%s=TRUE' % name.upper(), pah)
    # replace_or_append('export PRJ_IS_%s=TRUE' % name.upper(), 'export PRJ_IS_%s=TRUE' % name.upper(), pah)


    plug_prerequisites(name)
    plug_packages(name)


@task
def plug_all():
    for key, val in os.environ.items():
        if key[0:7] == 'PRJ_IS_' and val == 'TRUE':
            name = key[7:].lower()
            print "plugging '%s' apps group" % name
            plug_prerequisites(name)
            plug_packages(name)


@task
def project_setup():
    if not exists("/home/django/.virtualenvs/%s" % PRJ_NAME):
        run('mkvirtualenv %s' % (PRJ_NAME,))

    # Clono, se non e' gia stato clonato il progetto
    with cd("/home/django/"):
        if not exists(PRJ_NAME):
            sshagent_run('git clone %s %s' % (PRJ_GIT_REPO, PRJ_NAME))

        with prefix('workon %s' % PRJ_NAME):
            # Aggiungo all'ambiente virtuale la directory base del progetto e la directory apps
            run("add2virtualenv /home/django/%s" % PRJ_NAME)
            run("add2virtualenv /home/django/%s/external_apps" % PRJ_NAME)
            run("add2virtualenv /home/django/%s/website" % PRJ_NAME)

            with cd(PRJ_NAME):
                # Installo i pacchetti necessari
                run("pip install -r requirements/%s.txt" % env.name)

    # Creo il db
    remote_db_name = raw_input(u"db name for the %s db ? (defaults to project name) \n" % env.name)
    if len(remote_db_name.strip()) == 0:
        remote_db_name = PRJ_NAME

    remote_db_user = raw_input(u"username for the %s db ? (defaults to db name) \n" % env.name)
    if len(remote_db_user.strip()) == 0:
        remote_db_user = remote_db_name

    remote_db_pass = getpass.getpass(u"password for the %s db ? (defaults to username) \n" % env.name)
    if len(remote_db_pass.strip()) == 0:
        remote_db_pass = remote_db_user

    run("createuser -U postgres -d -R -S %s" % remote_db_user)
    run("createdb -U %s -h localhost %s" % (remote_db_user, remote_db_name))

    with cd("/home/django/%s/" % PRJ_NAME):
        run("touch .env")
        append(".env", "PRJ_ENV=%s" % env.name)
        append(".env", "PRJ_ENGINE=postgresql_psycopg2")
        append(".env", "PRJ_NAME=%s" % PRJ_NAME)
        append(".env", "PRJ_DB=%s" % PRJ_DB)
        append(".env", "PRJ_USER=%s" % PRJ_USER)
        append(".env", "PRJ_PASS=%s" % PRJ_PASS)
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
    with cd("/home/django/%s/etc" % PRJ_NAME):
        run("chmod +x gunicorn.sh")

    with cd("/etc/nginx/sites-enabled/"):
        run("ln -s /home/django/%s/etc/nginx.conf %s" % (PRJ_NAME, PRJ_NAME))

    with cd("/etc/supervisor/conf.d/"):
        run("ln -s /home/django/%s/etc/supervisor.conf %s.conf" % (PRJ_NAME, PRJ_NAME))

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
