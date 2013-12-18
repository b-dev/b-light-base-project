"""
WSGI config for testapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, site

repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
site.addsitedir(repo_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
