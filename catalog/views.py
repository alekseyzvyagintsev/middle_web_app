import os.path

from django.contrib import messages
from django.core.files.storage.filesystem import FileSystemStorage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.encoding import filepath_to_uri

from catalog.models import Product, Category
from config import settings


def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)  # Устанавливаем 12 продуктов на странице
    page_number = request.GET.get('page')  # Берём номер страницы из URL
    page_obj = paginator.get_page(page_number)  # Получаем нужную страницу
    context = {'page_obj': page_obj}
    return render(request, 'products/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'You have new message from {name}({email}): {message}')
    return render(request, 'products/contact.html')


def product_detail(request, product_id=1):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return redirect('catalog:home')

    cotext = {'product': product, }
    return render(request, 'products/product_detail.html', context=cotext)


def create_product(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_in = request.POST.get('category_name')
        price = request.POST.get('price')

        # Берём файл из request.FILES
        uploaded_image = request.FILES.get('image')

        # Проверка обязательных полей
        if not name or not description or not category_in or not price:
            messages.error(request, 'Все обязательные поля должны быть заполнены!')
            return render(request, 'products/create_product.html', context)

        try:
            # Получаем категорию
            category = Category.objects.get(name=category_in)

            # Обработка изображения
            if uploaded_image:
                # Сохраняем файл временно и присваиваем путь к новому товару
                fs = FileSystemStorage(location='media/product_images')
                filename = fs.save(uploaded_image.name, uploaded_image)
                img_path = f'product_images/{filename}'

                product = Product.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    price=price,
                    image=img_path
                )
            else:
                product = Product.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    price=price,
                    image='product_images/base_image.jpg'
                )

            messages.success(request, f'Вы успешно создали новый товар: {product.name}')
            return redirect('catalog:home')

        except Category.DoesNotExist:
            messages.error(request, f"Категория '{category_in}' не найдена.")
            return render(request, 'products/create_product.html', context)

        except Exception as e:
            messages.error(request, str(e))
            return render(request, 'products/create_product.html', context)

    return render(request, 'products/create_product.html', context)
