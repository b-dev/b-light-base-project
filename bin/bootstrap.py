import sys
import os
import random
import getpass

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

    _replace_in_vagrant_file(PRJ_ROOT,
                             {
                                 'PRJ_NAME' : PRJ_NAME,
                                 'PRJ_ENV' : PRJ_ENV,
                                 'PRJ_ENGINE' : 'postgresql_psycopg2',
                                 'PRJ_DB' : PRJ_DB,
                                 'PRJ_USER' : PRJ_USER,
                                 'PRJ_PASS' : PRJ_PASS
                             })

    env_path_file = os.path.join(REPO_ROOT, '.env')
    env_file = open(env_path_file, 'w')

    env_file.writelines(['export PRJ_ENV=%s\n' % PRJ_ENV,
                         'export PRJ_NAME=%s\n' % PRJ_NAME,
                         'export PRJ_ENGINE=%s\n' % 'postgresql_psycopg2',
                         'export PRJ_DB=%s\n' % PRJ_DB    ,
                         'export PRJ_USER=%s\n' % PRJ_USER,
                         'export PRJ_PASS=%s\n' % PRJ_PASS,
                         'export PRJ_SECRET_KEY="%s"' % "".join([random.choice(
                             "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_+)") for i in range(50)]),
                       ])
    env_file.close()
