import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_analyzer.settings")

celery_app = Celery("resume_analyzer")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
