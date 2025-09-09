#################################################################################################
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.files.storage.filesystem import FileSystemStorage
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
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


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("catalog:categories")
    permission_required = 'catalog.add_category'


class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("catalog:categories")
    permission_required = 'catalog.change_category'


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Category
    template_name = "products/category_detail.html"
    context_object_name = "category"
    permission_required = 'catalog.view_category'

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


class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Category
    template_name = "products/category_confirm_delete.html"
    success_url = reverse_lazy("catalog:categories")
    permission_required = 'catalog.delete_category'


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Category
    paginate_by = 12
    template_name = "products/categories.html"
    context_object_name = "categories"
    permission_required = 'catalog.view_category'

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by("-updated_at")


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, ImageHandlingMixin, SuccessMessageMixin,
                        CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_message = "Вы успешно создали новый товар!"
    success_url = reverse_lazy("catalog:products")
    permission_required = 'catalog.add_product'

    def form_valid(self, form):
        """
        Метод вызывается, когда форма прошла валидацию.
        Здесь мы добавляем текущего пользователя в качестве владельца товара.
        """
        # Получаем объект продукта из формы
        obj = form.save(commit=False)

        # Устанавливаем текущего пользователя в качестве владельца
        obj.owner = self.request.user

        # Сохраняем объект продукта в базе данных
        obj.save()

        # Возвращаем стандартный ответ родительского класса
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        if product.published is True:
            product.published = False
        else:
            product.published = True
        product.save()

        return redirect('catalog:products')


class ProductUpdateView(LoginRequiredMixin, ImageHandlingMixin, SuccessMessageMixin,
                        UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_message = "Вы успешно обновили товар!"
    success_url = reverse_lazy("catalog:products")

    def get_context_data(self, **kwargs):
        """Добавляем категории в контекст шаблона"""
        user = self.request.user
        if user == self.object.owner:
            context = super().get_context_data(**kwargs)
            context["categories"] = Category.objects.all()
            return context
        else:
            raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:products")

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект модели
        obj = self.get_object()

        # Проверяем, принадлежит ли пользователь группе Модераторов
        is_moderator = Group.objects.filter(name='Модератор продуктов', user=self.request.user).exists()

        # Если пользователь не является ни владельцем, ни модератором, запрещаем удаление
        if not (is_moderator or obj.owner == self.request.user):
            return PermissionDenied("Вы не имеете прав на удаление этого товара.")

        # Если проверка прошла успешно, выполняем стандартное удаление
        return super().dispatch(request, *args, **kwargs)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 12
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('catalog.can_unpublish_product'):
            queryset = super().get_queryset()  # Показываем ВСЕ товары, если у пользователя есть соответствующее право
        else:
            queryset = super().get_queryset().filter(
                owner=self.request.user)  # Иначе показываем только собственные товары
        return queryset.order_by('-updated_at')


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user  # Добавляем текущего пользователя в контекст
        return context

#################################################################################################
