#################################################################################################
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormMixin, UpdateView

from catalog.forms import CategoryForm, ProductForm
from catalog.models import Category, Product


class ImageHandlingMixin(FormMixin):
    def form_valid(self, form):
        """
        Общая логика обработки изображения и сохранение формы.
        """
        # проверяем, отмечено ли удаление изображения
        image_clear = self.request.POST.get("image-clear")
        # Получаем форму и добавляем обработку изображения
        uploaded_image = self.request.FILES.get("image")

        if uploaded_image:
            # Сохраняем изображение во временную директорию
            fs = FileSystemStorage(location="media/product_images")
            filename = fs.save(uploaded_image.name, uploaded_image)

            # Устанавливаем путь к изображению
            form.instance.image = f"product_images/{filename}"
        elif image_clear:
            # Если отметили удаление изображения, ставим None или пустую строку
            form.instance.image = ""
        else:
            # Если изображение не передано, устанавливаем базовую картинку
            form.instance.image = "product_images/base_image.jpg"

        # Возвращаем стандартный процесс сохранения
        return super().form_valid(form)


class HomeListView(ListView):
    model = Product
    paginate_by = 12
    template_name = "products/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by("-category")


class ContactView(View):
    def get(self, request):
        return render(request, "products/contact.html")

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"You have new message from {name}({phone}): {message}")
        return render(request, "products/contact.html")


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("catalog:categories")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("catalog:categories")


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "products/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        """Добавляем продукты данной категории в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        # Берём id текущей категории
        category_id = self.object.id
        # Фильтруем товары по текущей категории
        products_in_category = Product.objects.filter(category=category_id)
        # Передаём продукты в контекст
        context["products"] = products_in_category
        # Передаем количество товаров в категории
        context["product_count"] = len(products_in_category)
        return context


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "products/category_confirm_delete.html"
    success_url = reverse_lazy("catalog:categories")


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 12
    template_name = "products/categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by("-updated_at")


class ProductCreateView(LoginRequiredMixin, ImageHandlingMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_message = "Вы успешно создали новый товар!"
    success_url = reverse_lazy("catalog:products")

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, ImageHandlingMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_message = "Вы успешно обновили товар!"
    success_url = reverse_lazy("catalog:products")

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products")


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 12
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by("-updated_at")


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


#################################################################################################
