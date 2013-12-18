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

    PRJ_DB_NAME = raw_input(u"db name for the project local db ? (defaults to project name) \n")
    if len(PRJ_DB_NAME.strip()) == 0:
        PRJ_DB_NAME = PRJ_NAME

    PRJ_DB_USER = raw_input(u"username for the project local db ? (defaults to db name) \n")
    if len(PRJ_DB_USER.strip()) == 0:
        PRJ_DB_USER = PRJ_DB_NAME

    PRJ_DB_PASSWORD = getpass.getpass(u"password for the project local db ? (defaults to username) \n")
    if len(PRJ_DB_PASSWORD.strip()) == 0:
        PRJ_DB_PASSWORD = PRJ_DB_USER

    CREATE_DB = raw_input(u"you want the db created locally by me ?\n(if you plan to use vagrant say no, we'll create it on the guest later)\n[y/n]\n")
    if CREATE_DB in ('y', 'yes', 'Y', 'YES'):
        process = subprocess.Popen('export PGPASSWORD=%s && createdb -U %s -h localhost %s' % (PRJ_DB_PASSWORD, PRJ_DB_USER, PRJ_DB_NAME,),
                                   shell=True, executable="/bin/bash")

    _replace_in_file(PRJ_ROOT, 'etc/gunicorn.sh', {'%%PRJ_NAME%%': PRJ_NAME})
    _replace_in_file(PRJ_ROOT, 'etc/nginx.conf', {'%%PRJ_NAME%%': PRJ_NAME})
    _replace_in_file(PRJ_ROOT, 'etc/supervisor.conf', {'%%PRJ_NAME%%': PRJ_NAME})
    _replace_in_file(PRJ_ROOT, 'fabfile.py', {'%%PRJ_NAME%%': PRJ_NAME})
    _replace_in_file(PRJ_ROOT, 'website/settings/base.py', {'%%PRJ_NAME%%': PRJ_NAME})

    env_file_lines = [
        'export PRJ_ENV=%s' % PRJ_ENV,
        '\nexport PRJ_DB_NAME=%s' % PRJ_DB_NAME,
        '\nexport PRJ_DB_USER=%s' % PRJ_DB_USER,
        '\nexport PRJ_DB_PASSWORD=%s' % PRJ_DB_PASSWORD,
        '\nexport PRJ_SECRET_KEY="%s"' % "".join([random.choice(
         "abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_+)") for i in range(50)]),
        ]
    # for plugged_app_label in sys.argv[2:]:
    #     env_file_lines.append('\nexport PRJ_IS_%s=TRUE' % plugged_app_label.upper())

    INIT_GIT = raw_input(u"you just cloned the template project ? (I will remove current git config and create it from scratch in that case) \n[y/n]\n")
    if INIT_GIT in ('y', 'yes', 'Y', 'YES'):
        process = subprocess.Popen('cd %s && rm -f .hgignore' % PRJ_ROOT, shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        process = subprocess.Popen('cd %s && rm -fr .hg' % PRJ_ROOT, shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        process = subprocess.Popen('cd %s && rm -fr .git' % PRJ_ROOT, shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        process = subprocess.Popen('cd %s && git init' % PRJ_ROOT, shell=True, executable="/bin/bash")
        while process.poll() == None: pass
        PRJ_GIT_REPO = raw_input(u"repo url for the project ? (can be left empty and configured in git later) \n")
        _replace_in_file(PRJ_ROOT, 'Vagrantfile', {'PRJ_GIT_REPO' : PRJ_GIT_REPO})

        if PRJ_GIT_REPO:
            process = subprocess.Popen('cd %s && git remote add origin %s' % (PRJ_ROOT, PRJ_GIT_REPO),
                                       shell=True, executable="/bin/bash")
            while process.poll() == None: pass
        subprocess.Popen('cd %s && git add .' % PRJ_ROOT, shell=True, executable="/bin/bash")

        env_file_lines.append('\nexport PRJ_GIT_REPO=%s' % PRJ_GIT_REPO)

    with open(os.path.join(REPO_ROOT, '.env'), 'w') as env_file:
        env_file.writelines(env_file_lines)
