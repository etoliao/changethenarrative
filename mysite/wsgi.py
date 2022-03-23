"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

import dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()

# Load the environment variables, based on https://help.pythonanywhere.com/pages/environment-variables-for-web-apps

project_folder = os.path.expanduser('~/changethenarrative')
dotenv.read_dotenv(os.path.join('.env'))
SECRET_KEY = os.getenv("SECRET_KEY")