######################################################################################
from django.db import models

from users.models import CustomUser


class BlogEntry(models.Model):
    """
    Модель записи блога.

    Поля:
    - Заголовок (`title`)
    - Содержимое (`entry`)
    - Превью-изображение (`image`)
    - Дата создания (`created_at`)
    - Признак публикации (`is_active`)
    - Количество просмотров (`view_counter`)
    """

    title = models.CharField(max_length=200, null=False, blank=False, unique=True, verbose_name="Заголовок")
    entry = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    view_counter = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь", default=1)

    def __str__(self):
        state = "опубликована" if self.is_active else "удалена"
        return (
            f"{self.title}, "
            f"дата создания {self.created_at.strftime('%d-%m-%Y %H:%M')}, "
            f"количество просмотров {self.view_counter}, "
            f"состояние {state}"
        )

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ["title"]
        db_table = "article"


######################################################################################
