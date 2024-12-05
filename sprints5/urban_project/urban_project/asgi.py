"""
Конфигурация ASGI для проекта urban_project.

Она предоставляет вызываемый ASGI как переменную уровня модуля с именем ``application``.

Более подробную информацию об этом файле см. в
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_project.settings')

application = get_asgi_application()
