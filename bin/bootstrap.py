import sys, os
import random
import getpass

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_NAME = os.path.basename(REPO_ROOT)

if __name__ == '__main__':

    if len(sys.argv) < 1:
        print "Must give environment label"
        sys.exit()

    PRJ_ENV = sys.argv[1]
    PRJ_NAME = REPO_NAME
    PRJ_ROOT = REPO_ROOT.replace(REPO_NAME, PRJ_NAME)

    from sh import pip
    for line in pip.install('-r%s/requirements/%s.txt' % (PRJ_ROOT, PRJ_ENV), _iter=True):
        print line

    PRJ_DB = raw_input(u"db name for the project db ? (defaults to project name) \n")
    if len(PRJ_DB.strip()) == 0:
        PRJ_DB = PRJ_NAME

    PRJ_USER = raw_input(u"username for the project db ? (defaults to db name) \n")
    if len(PRJ_USER.strip()) == 0:
        PRJ_USER = PRJ_DB

    PRJ_PASS = getpass.getpass(u"password for the project db ? (defaults to username) \n")
    if len(PRJ_PASS.strip()) == 0:
        PRJ_PASS = PRJ_USER

    # os.environ['PRJ_ENV'] = PRJ_ENV
    # os.environ['DJANGO_SETTINGS_MODULE'] = PRJ_ENV
    # os.environ['PRJ_NAME'] = PRJ_NAME
    # os.environ['PRJ_DB'] = PRJ_DB
    # os.environ['PRJ_USER'] = PRJ_USER
    # os.environ['PRJ_PASS'] = PRJ_PASS
    # os.environ['PRJ_SECRET_KEY'] = "".join([random.choice(
    #     "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])
    #vhd = os.environ['VIRTUALENVWRAPPER_HOOK_DIR']

    env_path_file = os.path.join(REPO_ROOT, '.env')
    env_file = open(env_path_file, 'w')
    #lines = post_activate_hook.readlines()
    #for line in lines: pass
    env_file.writelines(['PRJ_ENV=%s\n' % PRJ_ENV,
                         'PRJ_NAME=%s\n' % PRJ_NAME,
                         'PRJ_DB=%s\n' % PRJ_DB    ,
                         'PRJ_USER=%s\n' % PRJ_USER,
                         'PRJ_PASS=%s\n' % PRJ_PASS,
                         'PRJ_SECRET_KEY="%s\n"' % "".join([random.choice(
                             "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_+)") for i in range(50)]),
                       ])
    env_file.close()
    #post_activate_hook.flush()
    #post_activate_hook.close()
