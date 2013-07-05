import sys
import os
import random
import getpass
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_NAME = os.path.basename(REPO_ROOT)

def _replace_in_vagrant_file(prj_root, dict):
    fpath = prj_root+"/Vagrantfile"
    with open(fpath) as f:
        s = f.read()
    s = s.replace('PRJ_NAME', dict['PRJ_NAME'])
    s = s.replace('PRJ_ENV', dict['PRJ_ENV'])
    s = s.replace('PRJ_ENGINE', dict['PRJ_ENGINE'])
    s = s.replace('PRJ_DB', dict['PRJ_DB'])
    s = s.replace('PRJ_USER', dict['PRJ_USER'])
    s = s.replace('PRJ_PASS', dict['PRJ_PASS'])
    with open(fpath, 'w') as f:
        f.write(s)

if __name__ == '__main__':

    if len(sys.argv) < 1:
        print "Must give environment label"
        sys.exit()

    PRJ_ENV = sys.argv[1]
    PRJ_NAME = REPO_NAME
    PRJ_ROOT = REPO_ROOT.replace(REPO_NAME, PRJ_NAME)

    PRJ_DB = raw_input(u"db name for the project db ? (defaults to project name) \n")
    if len(PRJ_DB.strip()) == 0:
        PRJ_DB = PRJ_NAME

    PRJ_USER = raw_input(u"username for the project db ? (defaults to db name) \n")
    if len(PRJ_USER.strip()) == 0:
        PRJ_USER = PRJ_DB

    PRJ_PASS = getpass.getpass(u"password for the project db ? (defaults to username) \n")
    if len(PRJ_PASS.strip()) == 0:
        PRJ_PASS = PRJ_USER

    PRJ_GIT_REPO = raw_input(u"repo url for the project ? \n")

    PRJ_ADDR_STAGING = raw_input(u"staging server address ? (can be left empty and filled in the .env file later) \n")
    if len(PRJ_ADDR_STAGING.strip()) == 0:
        PRJ_ADDR_STAGING = ''

    PRJ_ADDR_PRODUCTION = raw_input(u"production server address ? (can be left empty and filled in the .env file later) \n")
    if len(PRJ_ADDR_PRODUCTION.strip()) == 0:
        PRJ_ADDR_PRODUCTION = ''

    PRJ_ADDR_TEST = raw_input(u"test server address ? (can be left empty and filled in the .env file later) \n")
    if len(PRJ_ADDR_TEST.strip()) == 0:
        PRJ_ADDR_TEST = ''

    _replace_in_vagrant_file(PRJ_ROOT,
                             {
                                 'PRJ_NAME' : PRJ_NAME,
                                 'PRJ_ENV' : PRJ_ENV,
                                 'PRJ_ENGINE' : 'postgresql_psycopg2',
                                 'PRJ_DB' : PRJ_DB,
                                 'PRJ_USER' : PRJ_USER,
                                 'PRJ_PASS' : PRJ_PASS,
                                 'PRJ_GIT_REPO' : PRJ_GIT_REPO,
                                 'PRJ_ADDR_STAGING' : PRJ_ADDR_STAGING,
                                 'PRJ_ADDR_PRODUCTION' : PRJ_ADDR_PRODUCTION,
                                 'PRJ_ADDR_TEST' : PRJ_ADDR_TEST,
                             })

    with open(os.path.join(REPO_ROOT, '.env'), 'w') as env_file:
        env_file.writelines(['export PRJ_ENV=%s\n' % PRJ_ENV,
                             'export PRJ_NAME=%s\n' % PRJ_NAME,
                             'export PRJ_ENGINE=%s\n' % 'postgresql_psycopg2',
                             'export PRJ_DB=%s\n' % PRJ_DB    ,
                             'export PRJ_USER=%s\n' % PRJ_USER,
                             'export PRJ_PASS=%s\n' % PRJ_PASS,
                             'export PRJ_SECRET_KEY="%s"\n' % "".join([random.choice(
                                 "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_+)") for i in range(50)]),
                             'export PRJ_GIT_REPO=%s\n' % PRJ_GIT_REPO,
                             'export PRJ_ADDR_STAGING=%s\n' % PRJ_ADDR_STAGING,
                             'export PRJ_ADDR_PRODUCTION=%s\n' % PRJ_ADDR_PRODUCTION,
                             'export PRJ_ADDR_TEST=%s\n' % PRJ_ADDR_TEST,
                           ])

    process = subprocess.Popen('rm -f ../.hgignore', shell=True, executable="/bin/bash")
    while process.poll() == None: pass
    process = subprocess.Popen('rm -fr ../.hg', shell=True, executable="/bin/bash")
    while process.poll() == None: pass
    process = subprocess.Popen('rm -fr ../.git', shell=True, executable="/bin/bash")
    while process.poll() == None: pass
    process = subprocess.Popen('cd .. && git init', shell=True, executable="/bin/bash")
    while process.poll() == None: pass
    process = subprocess.Popen('cd .. && git remote add origin %s' % PRJ_GIT_REPO, shell=True, executable="/bin/bash")
    while process.poll() == None: pass
    subprocess.Popen('cd .. && git add .', shell=True, executable="/bin/bash")