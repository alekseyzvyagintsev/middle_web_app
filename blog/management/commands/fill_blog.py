import random

from django.core.management.base import BaseCommand

from blog.models import BlogEntry
from users.models import CustomUser


class Command(BaseCommand):
    help = "Заполняет таблицу блога тестовыми данными: по 3 записи от каждого пользователя"

    def handle(self, *args, **options):
        users = list(CustomUser.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING("Нет пользователей в базе данных. Сначала создайте пользователей."))
            return

        created_count = 0
        for user in users:
            for i in range(3):
                BlogEntry.objects.create(
                    title=f"Тестовый пост {random.randint(1, 1000)}",
                    entry=f"Тестовое содержание поста {random.randint(1, 1000)}",
                    user=user,
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Успешно создано {created_count} тестовых записей блога."))
