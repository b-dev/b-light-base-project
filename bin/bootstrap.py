import sys
import os
import random
import getpass
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_NAME = os.path.basename(REPO_ROOT)

def _replace_in_file(prj_root, file_name, dict):
    fpath = prj_root+"/"+file_name
    with open(fpath) as f:
        s = f.read()
    for key in dict.keys():
        s = s.replace(key, dict[key])
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

    _replace_in_file(PRJ_ROOT, 'Vagrantfile',
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
    _replace_in_file(PRJ_ROOT, 'etc/gunicorn.sh',
        {
            'PRJ_NAME' : PRJ_NAME,
        })
    _replace_in_file(PRJ_ROOT, 'etc/nginx.conf',
        {
            'PRJ_NAME' : PRJ_NAME,
        })
    _replace_in_file(PRJ_ROOT, 'etc/supervisor.conf',
        {
            'PRJ_NAME' : PRJ_NAME,
        })

    env_file_lines = [
        'export PRJ_ENV=%s' % PRJ_ENV,
        '\nexport PRJ_NAME=%s' % PRJ_NAME,
        '\nexport PRJ_ENGINE=%s' % 'postgresql_psycopg2',
        '\nexport PRJ_DB=%s' % PRJ_DB    ,
        '\nexport PRJ_USER=%s' % PRJ_USER,
        '\nexport PRJ_PASS=%s' % PRJ_PASS,
        '\nexport PRJ_SECRET_KEY="%s"' % "".join([random.choice(
         "abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_+)") for i in range(50)]),
        '\nexport PRJ_GIT_REPO=%s' % PRJ_GIT_REPO,
        '\nexport PRJ_ADDR_STAGING=%s' % PRJ_ADDR_STAGING,
        '\nexport PRJ_ADDR_PRODUCTION=%s' % PRJ_ADDR_PRODUCTION,
        '\nexport PRJ_ADDR_TEST=%s' % PRJ_ADDR_TEST,
        '\nexport PRJ_DEB_UPGRADE=TRUE',
        '\nexport PRJ_PIP_UPGRADE=TRUE',
        '\nexport PRJ_ASSETS_UPGRADE=TRUE',
        ]
    for plugged_app_label in sys.argv[2:]:
        env_file_lines.append('\nexport PRJ_IS_%s=TRUE' % plugged_app_label.upper())

    with open(os.path.join(REPO_ROOT, '.env'), 'w') as env_file:
        env_file.writelines(env_file_lines)

    INIT_GIT = raw_input(u"you just cloned the template project ? (I will remove current git config and create it from scratch in that case) \n[y/n]\n")
    if INIT_GIT in ('y', 'yes', 'Y', 'YES'):
        process = subprocess.Popen('rm -f ../.hgignore', shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        process = subprocess.Popen('rm -fr ../.hg', shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        process = subprocess.Popen('rm -fr ../.git', shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        process = subprocess.Popen('cd .. && git init', shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        if PRJ_GIT_REPO:
            process = subprocess.Popen('cd .. && git remote add origin %s' % PRJ_GIT_REPO,
                                       shell=True, executable="/bin/bash")
            while process.poll() == None: pass
        subprocess.Popen('cd .. && git add .', shell=True, executable="/bin/bash")