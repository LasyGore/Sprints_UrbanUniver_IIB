from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Advertisement, UserProfile


@receiver(post_save, sender=Advertisement)
def update_created_ads_count(sender, instance, created, **kwargs):
    """
    Обрабатывает сигнал после сохранения экземпляра объявления.

    Увеличивает счётчик созданных объявлений у пользователя, если объявление было создано.

    Аргументы:
        sender: Модель, отправившая сигнал.
        instance: Экземпляр объявления, который был создан или изменён.
        created (bool): Указывает, был ли экземпляр создан (True) или обновлён (False).
        kwargs: Дополнительные аргументы.
    """
    if created:
        # Убедимся, что у пользователя есть профиль
        user_profile, _ = UserProfile.objects.get_or_create(user=instance.author)
        user_profile.created_ads_count += 1  # Увеличиваем счетчик созданных объявлений
        user_profile.save()


@receiver(post_delete, sender=Advertisement)
def update_deleted_ads_count(sender, instance, **kwargs):
    """
    Обрабатывает сигнал после удаления экземпляра объявления.

    Увеличивает счётчик удалённых объявлений у пользователя.

    Аргументы:
        sender: Модель, отправившая сигнал.
        instance: Экземпляр объявления, который был удалён.
        kwargs: Дополнительные аргументы.
    """
    # Убедимся, что у пользователя есть профиль
    user_profile, _ = UserProfile.objects.get_or_create(user=instance.author)
    user_profile.deleted_ads_count += 1  # Увеличиваем счетчик удалённых объявлений
    user_profile.save()
