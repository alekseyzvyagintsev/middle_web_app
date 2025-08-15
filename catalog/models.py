from django.db import models


class Category(models.Model):
    """Класс
    наименование,
    описание.
    """

    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name="Имя категории")
    description = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]
        db_table = "category"


class Product(models.Model):
    """
    наименование,
    описание,
    изображение,
    категория,
    цена за покупку,
    дата создания,
    дата последнего изменения.
    """

    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name="Имя продукта")
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.FloatField(default=0.0, verbose_name="цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} {self.name} {self.price}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name"]
        db_table = "product"
