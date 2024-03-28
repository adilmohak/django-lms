"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

#Add virtual environment for site
sys.path.insert(0,'/var/www/django-lms')
sys.path.insert(0,'/var/www/django-lms/config')
sys.path.insert(0,'/var/www/django-lms/venv/lib/python3.10/site-packages')
print(sys.path)
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
