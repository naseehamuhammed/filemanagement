from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_management.settings")
app = Celery("file_management")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(['gallery'])