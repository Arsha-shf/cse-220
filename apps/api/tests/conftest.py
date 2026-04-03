"""Unit tests configuration module."""

import os

import django
from django.conf import settings

from config.bootstrap import configure_workspace_paths

configure_workspace_paths()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

if "testserver" not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = [*settings.ALLOWED_HOSTS, "testserver"]
