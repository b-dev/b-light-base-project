import os, time, random, getpass
from os.path import abspath, dirname, isfile

from fabric.api import *
from fabric.contrib.files import append, exists

PROJECT_ROOT = dirname(abspath(__file__))

from _set_local_env_vars import import_env_vars
import_env_vars(PROJECT_ROOT)

PRJ_ENV = os.environ['PRJ_ENV']
PRJ_NAME = '%%PRJ_NAME%%'

PRJ_GIT_REPO = os.getenv('PRJ_GIT_REPO')

ENVIRONMENTS = {
    'dev': ['127.0.0.1'],
    'staging': '',
    'production': '',
    'test': '',
}

env.user = 'django'
# to enable ssh key forwarding
env.forward_agent = True

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
def bower():
    from sh import bower
    pah = os.path.join(PROJECT_ROOT, 'requirements', 'front_base.txt')
    with open(pah, 'r') as reqfile:
        for line in reqfile:
            bower.install(line.strip())


@task
def plug_prerequisites(name):
    env.user = 'vagrant'
    path = os.path.join(PROJECT_ROOT, 'etc', 'install', 'plug_%s.pkg' % name)
    packages_to_install = []
    if not os.path.exists(path):
        return
    with open(path, 'r') as pkgs_file:
        lines = pkgs_file.readlines()
        for line in lines:
            if len(line) and not line[0:1] == '#':
                packages_to_install.append(line.strip())
    require.deb.packages(packages_to_install)


@task
def plug(name):
    # TODO : da riabilitare. Disabilitato perche' mi da errore che non trova fabtools (e non voglio installarlo globalmente)
    # plug_prerequisites(name)

    with prefix(". /usr/local/bin/virtualenvwrapper.sh; workon %s" % PRJ_NAME):
        local("pip install -r %s/requirements/apps/%s.txt" % (PROJECT_ROOT, name))

        # Enable the plugged app inside the settings
        lines = []
        app_enabled = False
        for line in open(os.path.join(PROJECT_ROOT, 'website', 'settings', 'base.py'), 'r').readlines():
            if line.find('PRJ_ENABLE_%s = False' % name.upper()) > -1:
                line = 'PRJ_ENABLE_%s = True\n' % name.upper()
                app_enabled = True
            lines.append(line)

        # Rewrite the correct settings file with appname enabled (only if it was enabled)
        if app_enabled:
            new_settings = open(os.path.join(PROJECT_ROOT, 'website', 'settings', 'base.py'), 'w')
            new_settings.writelines(lines)
            new_settings.close()

        local("python %s/manage.py syncdb --all" % PROJECT_ROOT)
        local("python %s/manage.py migrate --fake" % PROJECT_ROOT)


@task
def project_setup():
    if not exists("/home/django/.virtualenvs/%s" % PRJ_NAME):
        run('mkvirtualenv %s' % (PRJ_NAME,))

    # Clono, se non e' gia stato clonato il progetto
    with cd("/home/django/"):
        if not exists(PRJ_NAME):
            run('git clone %s %s' % (PRJ_GIT_REPO, PRJ_NAME))

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
        append(".env", "PRJ_DB_NAME=%s" % remote_db_name)
        append(".env", "PRJ_DB_USER=%s" % remote_db_user)
        append(".env", "PRJ_DB_PASSWORD=%s" % remote_db_pass)
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
        run("git pull")
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
def reload_supervisor():
    env.user = 'root'
    run('supervisorctl reload')


@task
def restart_server():
    env.user = 'root'
    run('/etc/init.d/nginx restart')
    run("/etc/init.d/supervisor stop")
    time.sleep(5)
    run("/etc/init.d/supervisor start")
