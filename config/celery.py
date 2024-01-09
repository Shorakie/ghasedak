import os

from celery import Celery
from decouple import config
from django.apps import apps, AppConfig
from django.conf import settings

if not settings.configured:
    environment = config('ENVIRONMENT')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings." + environment)

APP = Celery('config')


class CeleryConfig(AppConfig):
    name = 'config'
    verbose_name = 'Celery Config'

    def ready(self):
        APP.config_from_object('django.conf:settings', namespace='CELERY')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        APP.conf.update(broker_connection_retry_on_startup=True)
        if settings.DEBUG:
            APP.conf.update(task_always_eager=True)

        APP.autodiscover_tasks(installed_apps, force=True)
