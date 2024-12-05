"""
Конфигурация WSGI для проекта urban_project.
Она представляет вызываемый WSGI как переменную уровня модуля с именем ``application``.
Для получения дополнительной информации об этом файле см.
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_project.settings')

application = get_wsgi_application()
