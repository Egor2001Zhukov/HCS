from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hcs.settings')

# Создание экземпляра объекта Celery
app = Celery('hcs')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()
