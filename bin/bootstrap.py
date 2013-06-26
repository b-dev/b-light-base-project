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

    env_path_file = os.path.join(REPO_ROOT, '.env')
    env_file = open(env_path_file, 'w')

    env_file.writelines(['PRJ_ENV=%s\n' % PRJ_ENV,
                         'PRJ_NAME=%s\n' % PRJ_NAME,
                         'PRJ_DB=%s\n' % PRJ_DB    ,
                         'PRJ_USER=%s\n' % PRJ_USER,
                         'PRJ_PASS=%s\n' % PRJ_PASS,
                         'PRJ_SECRET_KEY="%s"' % "".join([random.choice(
                             "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_+)") for i in range(50)]),
                       ])
    env_file.close()

    # add2virtualenv
    import distutils
    SITE_PACKAGES_DIR = distutils.sysconfig.get_python_lib()
    file_pth_path = os.path.join(SITE_PACKAGES_DIR, '_virtualenv_path_extensions.pth')
    file_pth = open(file_pth_path, 'w')
    file_pth.writelines([
        "import sys; sys.__plen = len(sys.path)\n",
        "%s\n" % os.path.abspath('website'),
        "%s\n" % os.path.abspath('external_apps'),
        "%s\n" % os.path.abspath('.'),
        "import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)"
    ])
