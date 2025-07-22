from django.urls import path
from catalog.apps import CatalogConfig
from . import views
from .views import product_detail, create_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('create_product/', views.create_product, name='create_product')
]
