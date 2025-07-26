from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage.filesystem import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin

from blog.models import BlogEntry


class ArticleForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ['title', 'entry', 'image', 'is_active']


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
            fs = FileSystemStorage(location='media/blog_images')
            filename = fs.save(uploaded_image.name, uploaded_image)

            # Устанавливаем путь к изображению
            form.instance.image = f'blog_images/{filename}'
        elif image_clear:
            # Если отметили удаление изображения, ставим None или пустую строку
            form.instance.image = ''
        else:
            # Если изображение не передано, устанавливаем базовую картинку
            form.instance.image = 'blog_images/base_blog_image.jpg'

        # Возвращаем стандартный процесс сохранения
        return super().form_valid(form)


class ActiveArticlesListView(ListView):
    model = BlogEntry
    paginate_by = 12
    template_name = 'blog/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        queryset = super().get_queryset()  # Базовый набор продуктов
        return queryset.order_by('-is_active')


class ArchiveArticlesListView(ListView):
    model = BlogEntry
    paginate_by = 12
    template_name = 'blog/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        # Сначала получаем все неактивные статьи
        queryset = super().get_queryset().filter(is_active=False)

        # Затем сортируем их по дате создания (от новых к старым)
        return queryset.order_by('-created_at')


class BlogEntryCreateView(ImageHandlingMixin, CreateView):
    model = BlogEntry
    form_class = ArticleForm
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        # Определение URL после успешной операции
        return reverse_lazy('blog:entry_detail', kwargs={'pk': self.object.pk})


class BlogEntryUpdateView(ImageHandlingMixin, UpdateView):
    model = BlogEntry
    form_class = ArticleForm
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        # Определение URL после успешной операции
        return reverse_lazy('blog:entry_detail', kwargs={'pk': self.object.pk})


class ContactsView(View):
    def get(self, request):
        return render(request, 'blog/contacts.html')

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({phone}): {message}')
        return render(request, 'blog/contacts.html')


class BlogEntryDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/entry_detail.html'
    context_object_name = 'blog_entry'

    def get_object(self, queryset=None):
        # Получаем объект записи блога
        obj = super().get_object(queryset)

        # Увеличение счётчика просмотров
        obj.view_counter += 1
        obj.save(update_fields=['view_counter'])

        return obj


class BlogEntryDeleteView(DeleteView):
    model = BlogEntry
    template_name = 'blog/entry_delete.html'
    success_url = reverse_lazy('blog:active_articles')
