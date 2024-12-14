from django import forms
from .models import Advertisement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AdvertisementForm(forms.ModelForm):
    """
    Форма для создания и редактирования объявления.

    Класс наследуется от ModelForm и автоматически генерирует форму на основе
    модели Advertisement.

    Атрибуты:
        Meta (класс): Внутренний класс, определяющий модель и поля формы.
    """

    class Meta:
        model = Advertisement  # Модель, на основе которой создается форма
        fields = ['title', 'content', 'author', 'image']  # Поля модели, которые будут включены в форму


class SignUpForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя.

    Класс наследуется от UserCreationForm, который предоставляет функциональность
    для создания нового пользователя с использованием стандартных полей
    (имя пользователя и пароль).

    Атрибуты:
        Meta (класс): Внутренний класс, определяющий модель и поля формы.
    """

    class Meta:
        model = User  # Модель, на основе которой создается форма
        fields = ('username', 'password1', 'password2',)  # Поля для регистрации
