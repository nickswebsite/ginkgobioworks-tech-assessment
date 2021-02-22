import os
import threading

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery("ginkgo_bioworks_tech_assessment")

app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()


def start_memory_broker():
    worker = app.Worker(app=app, bool='solo', concurrency=1)
    thread = threading.Thread(target=worker.start)
    thread.daemon = True
    thread.start()


if app.conf.broker_url.startswith("memory://"):
    start_memory_broker()
