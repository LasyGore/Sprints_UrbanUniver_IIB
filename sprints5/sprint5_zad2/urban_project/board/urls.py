from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('advertisement/<int:pk>/edit/', views.edit_advertisement, name='edit_advertisement'),  # Новый URL для редактирования
    path('advertisement/<int:pk>/delete/', views.delete_advertisement, name='delete_advertisement'),  # Новый URL для удаления объявления
]

