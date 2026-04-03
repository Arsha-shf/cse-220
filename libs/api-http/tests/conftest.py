"""Test setup for api-http library tests."""

import os
import sys
from pathlib import Path

import django

ROOT = Path(__file__).resolve().parents[3]
API_APP_ROOT = ROOT / "apps" / "api"

if str(API_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(API_APP_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
