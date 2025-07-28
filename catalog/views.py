from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin

from catalog.models import Product, Category


class HomeListView(ListView):
    model = Product
    paginate_by = 12
    template_name = 'products/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by('-category')


class ContactView(View):
    def get(self, request):
        return render(request, 'products/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}): {message}')
        return render(request, 'products/contact.html')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']


class ImageHandlingMixin(FormMixin):
    def form_valid(self, form):
        """
        Общая логика обработки изображения и сохранение формы.
        """
        # проверяем, отмечено ли удаление изображения
        image_clear = self.request.POST.get('image-clear')
        # Получаем форму и добавляем обработку изображения
        uploaded_image = self.request.FILES.get('image')

        if uploaded_image:
            # Сохраняем изображение во временную директорию
            fs = FileSystemStorage(location='media/product_images')
            filename = fs.save(uploaded_image.name, uploaded_image)

            # Устанавливаем путь к изображению
            form.instance.image = f'product_images/{filename}'
        elif image_clear:
            # Если отметили удаление изображения, ставим None или пустую строку
            form.instance.image = ''
        else:
            # Если изображение не передано, устанавливаем базовую картинку
            form.instance.image = 'product_images/base_image.jpg'

        # Возвращаем стандартный процесс сохранения
        return super().form_valid(form)


class ProductCreateView(ImageHandlingMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create_product.html'
    success_message = 'Вы успешно создали новый товар!'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        """ Добавляем категории в контекст шаблона """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    paginate_by = 12
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by('-updated_at')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(ImageHandlingMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create_product.html'
    success_message = 'Вы успешно обновили товар!'
    success_url = reverse_lazy('catalog:product_list')

    def get_context_data(self, **kwargs):
        """ Добавляем категории в контекст шаблона """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
