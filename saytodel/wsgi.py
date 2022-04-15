"""
WSGI config for Samodelkin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import subprocess

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Samodelkin.settings')

subprocess.Popen(['./manage.py', 'inn_verification'])

application = get_wsgi_application()
