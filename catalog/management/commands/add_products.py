from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Добавление продуктов в базу данных"

    def handle(self, *args, **options):
        category, _ = Category.objects.get_or_create(name="tv", description="Телевизоры")

        products = [
            {
                "name": "Haier",
                "description": 'Телевизор 55 Smart TV M1 55" 4K UHD, черно-серый',
                "category": category,
                "price": "30000",
            },
            {
                "name": "STARWIND",
                "description": 'Телевизор SW-LED58UG401 58" 4K UHD, серый металлик',
                "category": category,
                "price": "29000",
            },
            {
                "name": "Hartens",
                "description": 'Телевизор HT-32H06B-VZ/M 32" HD, черный',
                "category": category,
                "price": "10000",
            },
            {
                "name": "TLC",
                "description": 'Телевизор 75V6B 75" 4K UHD, черный',
                "category": category,
                "price": "49500",
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Продукт {product.name} добавлен успешно."))
            else:
                self.stdout.write(self.style.WARNING(f"Продукт {product.name} уже существует."))
