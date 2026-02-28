import os
from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "myshop.settings.base"  # ← дефолт для локальной разработки
)

app = Celery("myshop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()