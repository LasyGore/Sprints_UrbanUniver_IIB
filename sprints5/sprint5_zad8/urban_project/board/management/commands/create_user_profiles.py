from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from board.models import UserProfile

class Command(BaseCommand):
    help = 'Создает UserProfile для всех существующих пользователей'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('UserProfile успешно создан для всех пользователей.'))