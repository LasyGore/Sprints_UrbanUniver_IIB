from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    """
    Модель объявления.

    Атрибуты:
        title (CharField): Заголовок объявления, максимальная длина 255 символов.
        content (TextField): Содержимое объявления.
        author (ForeignKey): Пользователь, создавший объявление (внешний ключ на модель User).
        created_at (DateTimeField): Дата и время создания объявления (автоматически добавляется).
        image (ImageField): Изображение объявления, загружается в папку 'advertisements/',
                            может быть null или пустым.
        like:  Поле для подсчета лайков;
        dislike:  Поле для подсчета дизлайков;
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='advertisements/', null=True, blank=True)
    likes = models.IntegerField(default=0)  # Поле для подсчета лайков
    dislikes = models.IntegerField(default=0)  # Поле для подсчета дизлайков


    def __str__(self):
        """
        Возвращает строковое представление объявления.

        Возвращает:
            str: Заголовок объявления.
        """
        return self.title


class Comment(models.Model):
    """
    Модель комментария к объявлению.

    Атрибуты:
        advertisement (ForeignKey): Объявление, к которому принадлежит комментарий
                                    (внешний ключ на модель Advertisement).
        author (ForeignKey): Пользователь, оставивший комментарий (внешний ключ на модель User).
        content (TextField): Содержимое комментария.
        created_at (DateTimeField): Дата и время создания комментария (автоматически добавляется).
    """
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление комментария.

        Возвращает:
            str: Строка в формате 'Комментарий от {автор} к {объявлению}'.
        """
        return f'Comment by {self.author} on {self.advertisement}'


class UserProfile(models.Model):
    """
    Модель профиля пользователя.

    Эта модель хранит статистику пользователя, включая общее количество созданных и удалённых объявлений,
    а также количество лайков и дизлайков, выставленных пользователем.

    Атрибуты:
        user (OneToOneField): Связь с моделью User.
        created_ads_count (PositiveIntegerField): Количество объявлений, созданных пользователем.
        deleted_ads_count (PositiveIntegerField): Количество объявлений, удалённых пользователем.
        likes_count (PositiveIntegerField): Общее количество лайков, выставленных пользователем.
        dislikes_count (PositiveIntegerField): Общее количество дизлайков, выставленных пользователем.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_ads_count = models.PositiveIntegerField(default=0)
    deleted_ads_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Возвращает строковое представление профиля пользователя, отображая имя пользователя.
        """
        return self.user.username