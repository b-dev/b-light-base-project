import sys, os
import random

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_NAME = os.path.basename(REPO_ROOT)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Must give project name as first argument"
        sys.exit()
    try:
        PRJ_ENV = sys.argv[2]
    except:
        PRJ_ENV = 'dev'

    PRJ_NAME = sys.argv[1]
    PRJ_ROOT = REPO_ROOT.replace(REPO_NAME, PRJ_NAME)

    if REPO_ROOT != PRJ_ROOT:
        from sh import mv
        mv(REPO_ROOT, PRJ_ROOT)

    from sh import pip
    for line in pip.install('-r%s/requirements/%s.txt' % (PRJ_ROOT, PRJ_ENV), _iter=True):
        print line

    PRJ_DB = raw_input(u"db name for the project db ? (defaults to project name) \n")
    if len(PRJ_DB.strip()) == 0:
        PRJ_DB = PRJ_NAME

    PRJ_USER = raw_input(u"username for the project db ? (defaults to db name) \n")
    if len(PRJ_USER.strip()) == 0:
        PRJ_USER = PRJ_DB

    PRJ_PASS = raw_input(u"password for the project db ? (defaults to username) \n")
    if len(PRJ_PASS.strip()) == 0:
        PRJ_PASS = PRJ_USER

    os.environ['PRJ_ENV'] = PRJ_ENV
    os.environ['DJANGO_SETTINGS_MODULE'] = PRJ_ENV
    os.environ['PRJ_NAME'] = PRJ_NAME
    os.environ['PRJ_DB'] = PRJ_DB
    os.environ['PRJ_USER'] = PRJ_USER
    os.environ['PRJ_PASS'] = PRJ_PASS
    os.environ['PRJ_SECRET_KEY'] = "".join([random.choice(
        "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)])

    vhd = os.environ['VIRTUALENVWRAPPER_HOOK_DIR']
    pah = os.path.join(vhd, PRJ_NAME, 'bin', 'postactivate')
    post_activate_hook = open(pah, 'r+')
    lines = post_activate_hook.readlines()
    for line in lines: pass
    post_activate_hook.writelines(['export PRJ_ENV=%s\n' % PRJ_ENV,
                                   'export DJANGO_SETTINGS_MODULE=settings.%s\n' % PRJ_ENV,
                                   'export PRJ_NAME=%s\n' % PRJ_NAME,
                                   'export PRJ_DB=%s\n' % PRJ_DB    ,
                                   'export PRJ_USER=%s\n' % PRJ_USER,
                                   'export PRJ_PASS=%s\n' % PRJ_PASS,
                                   'export PRJ_SECRET_KEY="%s\n"' % "".join([random.choice(
                                       "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_+)") for i in range(50)]),
                                   ])
    post_activate_hook.flush()
    post_activate_hook.close()
