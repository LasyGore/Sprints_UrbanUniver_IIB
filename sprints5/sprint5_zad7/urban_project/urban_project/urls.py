"""
Конфигурация URL для проекта urban_project.
Список `urlpatterns` направляет URL в представления. Для получения дополнительной информации см.:
https://docs.djangoproject.com/en/5.0/topics/http/urls/
Примеры:
Функциональные представления
1. Добавьте импорт: from my_app import views
2. Добавьте URL в urlpatterns: path('', views.home, name='home')
Представления на основе классов
1. Добавьте импорт: from other_app.views import Home
2. Добавьте URL в urlpatterns: path('', Home.as_view(), name='home')
Включение другого URLconf
1. Импортируйте функцию include(): from django.urls import include, path
2. Добавьте URL в urlpatterns: path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from board import views as board_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls', namespace='board')),
    path('accounts/logout/', board_views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', board_views.home, name='home'),
    path('signup/', board_views.signup, name='signup'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
