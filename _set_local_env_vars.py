import os

def import_env_vars(project_root):
    """Imports some environment variables from a special .env file in the
    project root directory.
    """
    if len(project_root) > 0 and project_root[-1] != '/':
        project_root += '/'
    try:
        envfile = open(project_root+'.env')
    except IOError:
        # If there isn't an env file don't raise any error. Maybe you override settings by the local.py file
        return

    for line in envfile.readlines():
        if len(line) > 1 and not line[0:1] == '#':
            [key,value] = line.replace('export ', '').strip().split("=")
            os.environ[key] = value
