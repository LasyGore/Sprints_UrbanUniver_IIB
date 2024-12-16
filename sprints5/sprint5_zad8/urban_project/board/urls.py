from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('advertisement/<int:pk>/edit/', views.edit_advertisement, name='edit_advertisement'),  # Новый URL для редактирования
    path('advertisement/<int:pk>/delete/', views.delete_advertisement, name='delete_advertisement'),  # Новый URL для удаления объявления
    path('advertisement/<int:pk>/like/', views.like_advertisement, name='like_advertisement'),   # Новый URL для лайка
    path('advertisement/<int:pk>/dislike/', views.dislike_advertisement, name='dislike_advertisement'),  # Новый URL для дизлайка
]

"""
URL-шаблоны для приложения 'board'.

Доступные маршруты:
- '' (Путь к списку объявлений)
- 'advertisement/<int:pk>/' (Путь к деталям объявления по его первичному ключу)
- 'add/' (Путь к форме добавления нового объявления)
- 'advertisement/<int:pk>/edit/' (Путь к форме редактирования существующего объявления по его первичному ключу)
- 'advertisement/<int:pk>/delete/' (Путь к форме удаления объявления по его первичному ключу)
- 'advertisement/<int:pk>/like/' (Путь к форме для лайка )
- 'advertisement/<int:pk>/dislike/' (Путь к форме для дизлайка) 
"""
