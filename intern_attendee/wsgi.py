"""
WSGI config for intern_attendee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intern_attendee.settings')

application = get_wsgi_application()
