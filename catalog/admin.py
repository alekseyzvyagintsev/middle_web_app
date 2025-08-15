from django.contrib import admin

from .models import Category, Product


# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_filter = (
        "name",
        "id",
    )
    search_fields = (
        "name",
        "description",
    )


# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "image",
    )
    list_filter = (
        "price",
        "id",
    )
    search_fields = (
        "name",
        "category__name",
    )
