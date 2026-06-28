"""WSGI entrypoint for the Django project.

This file provides the standard WSGI `application` callable referenced
by `WSGI_APPLICATION` in the project's settings.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings")

application = get_wsgi_application()
