from django.contrib import admin
from .models import Advertisement, Comment

"""
        Модуль admin.py

        Этот модуль предназначен для регистрации моделей в административной панели Django.
        Зарегистрированные модели будут доступны для управления через интерфейс администратора.
"""

# Регистрируем модель Advertisement в административной панели
admin.site.register(Advertisement)

# Регистрируем модель Comment в административной панели
admin.site.register(Comment)