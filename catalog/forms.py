#########################################################################################################
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import BooleanField

from .models import Category, Product
from .validators import validate_extensions, validate_forbidden_words, validate_max_size_mb

TABOO = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class StileFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class CategoryForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

    def clean_name(self):
        """Метод очистки и проверки поля 'name'"""
        data = self.cleaned_data["name"].lower()  # приводим строку к нижнему регистру
        validate_forbidden_words(TABOO, data)
        return data

    def clean_description(self):
        """Метод очистки и проверки поля 'description'"""
        data = self.cleaned_data["description"].lower()  # приводим строку к нижнему регистру
        validate_forbidden_words(TABOO, data)
        return data


class ProductForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "image"]

    def clean_name(self):
        """Метод очистки и проверки поля 'name'"""
        data = self.cleaned_data["name"].lower()
        validate_forbidden_words(TABOO, data)
        return data

    def clean_description(self):
        """Метод очистки и проверки поля 'description'"""
        data = self.cleaned_data["description"].lower()
        validate_forbidden_words(TABOO, data)
        return data

    def clean_price(self):
        """Метод очистки и проверки поля 'price'"""
        data = self.cleaned_data["price"]
        if float(data) < 0:
            raise ValidationError(f'Запрещено использовать отрицательные числа "{data}".')
        return data

    def clean_image(self):
        """Метод очистки и проверки поля 'image'"""
        image_field = self.cleaned_data["image"]
        # пропускаем пустое поле
        if not image_field:
            return None
        # Проверяем файлы на соответствие допустимым расширениям
        valid_extensions = ["jpeg", "png"]
        validate_extensions(valid_extensions, image_field)
        # Проверяем, что размер файла не превышает допустимый размер
        max_size_mb = 5
        validate_max_size_mb(max_size_mb, image_field)

        return image_field

#########################################################################################################
