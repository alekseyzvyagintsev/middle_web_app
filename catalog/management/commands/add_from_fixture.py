import json

from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Импорт товаров и категорий из файла в базу данных."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="catalog_fixture.json",
            help="Путь к файлу JSON с товарами и категориями.",
        )

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        file_path = options["file"]

        try:
            with open(file_path, encoding="utf-8") as file:
                data = json.load(file)

            categories = {}
            products = []

            # Разделяем данные на категории и товары
            for item in data:
                model_name = item.pop("model")

                if model_name == "catalog.category":
                    fields = item.pop("fields")

                    # Создаем объекты категорий и сохраняем их для последующего использования
                    category, _ = Category.objects.get_or_create(id=item["pk"], defaults=fields)
                    categories[item["pk"]] = category

                    self.stdout.write(self.style.SUCCESS(f"Категория '{category.name}' добавлена."))

                elif model_name == "catalog.product":
                    fields = item.pop("fields")
                    products.append((item["pk"], fields))  # Сохраняем ID товара и его данные для последующей обработки

            # Обрабатываем товары, учитывая ранее созданные категории
            for pk, product_data in products:
                category_id = product_data.pop("category")
                category = categories.get(category_id)

                if category is None:
                    raise ValueError(f"Категория с ID={category_id} не найдена.")

                # Создаем товар, связывая его с категорией
                product, _ = Product.objects.get_or_create(id=pk, defaults={**product_data, "category": category})

                self.stdout.write(self.style.SUCCESS(f"Товар '{product.name}' добавлен."))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Файл '{file_path}' не найден."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(str(e)))
