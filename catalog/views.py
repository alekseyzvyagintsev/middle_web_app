from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse


from catalog.models import Product, Category


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
    context = {'categories': categories,}
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_name = request.POST.get('category_choice')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        if not name or not description or not category_name or not price:
            messages.error(request, 'Все обязательные поля должны быть заполнены!')
            return render(request, 'products/create_product.html', context)
        else:
            try:
                price_value = float(price)
                if image:
                    product = Product.objects.create(
                        name=name,
                        description=description,
                        category=category_name,
                        price=price_value,
                        image=image
                    )
                else:
                    product = Product.objects.create(
                        name=name,
                        description=description,
                        category=category_name,
                        price=price_value,
                        image='static/images/base_image.jpg'
                    )
                messages.success(request, f'Вы успешно создали новый товар: {product.name}')
                return redirect('catalog:home')
            except ValueError:
                messages.error(request, 'Цена указана неверно.')
            except Exception as e:
                messages.error(request, str(e))
    return render(request, 'products/create_product.html', context)
