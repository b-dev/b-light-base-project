import os, sh
from fabric.api import *
from fabtools import require
import fabtools


PRJ_ENV = os.environ['PRJ_ENV']
PRJ_NAME = os.environ['PRJ_NAME']
PRJ_DB = os.environ['PRJ_DB']
PRJ_USER = os.environ['PRJ_USER']
PRJ_PASS = os.environ['PRJ_PASS']


ENVIRONMENTS = {
    'dev': ['127.0.0.1'],
    'staging': ['placehold-staging'],
    'production': ['placehold-production'],
}

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
def configure_db():
    if env.name == 'dev':
        # TODO
        return

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


################
# Environment SETUPS
###############

#
# # sshagent_run credits to http://lincolnloop.com/blog/2009/sep/22/easy-fabric-deployment-part-1-gitmercurial-and-ssh/
# # modified by dvd :)
# def sshagent_run(cmd, capture=True):
#     """
#     Helper function.
#     Runs a command with SSH agent forwarding enabled.
#
#     Note:: Fabric (and paramiko) can't forward your SSH agent.
#     This helper uses your system's ssh to do so.
#     """
#
#     cwd = env.get('cwd', '')
#     if cwd:
#         cmd = 'cd %s;%s' % (cwd, cmd)
#
#     with settings(cwd=''):
#         for h in env.hosts:
#             try:
#                 # catch the port number to pass to ssh
#                 host, port = h.split(':')
#                 local('ssh -p %s -A %s@%s "%s"' % (port, env.user, host, cmd), capture=capture)
#             except ValueError:
#                 local('ssh -A %s@%s "%s"' % (env.user, h, cmd), capture=capture)
#
# def dev():
#     env.name = 'dev'
#     env.hosts = ENVIRONMENTS[env.name]
#
# def staging():
#     env.name = 'staging'
#     env.hosts = ENVIRONMENTS[env.name]
#
# def production():
#     env.name = 'production'
#     env.hosts = ENVIRONMENTS[env.name]
#
# def update():
#     # Clono, se non e' gia stato clonato il progetto
#     with cd("/home/django/%s" % PROJECT_NAME):
#         sshagent_run("hg pull -u")
#         with prefix('workon %s' % PROJECT_NAME):
#             run("python website/manage.py migrate")
#             run("python website/manage.py collectstatic --noinput")
#
#     env.user = 'root'
#     run('supervisorctl reload')
#
# def restart_server():
#     env.user = 'root'
#     run('/etc/init.d/nginx restart')
#     run('/etc/init.d/supervisor restart')
#
#

#
#     # SE SI HANNO PROBLEMI CON PIL PERCHE NON INSTALLA IL SUPPORTO AL JPEG (TENDENZIALMENTE IL PROBLEMA
#     # SI HA CON LE VERSIONI A 64 BIT) CREARE I SEGUENTI LINK SIMBOLICI:
#     # ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
#     # ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
#     # ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
#
