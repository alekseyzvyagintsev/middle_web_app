from django.urls import path
from catalog.apps import CatalogConfig
from .views import (ProductCreateView,
                    ProductListView,
                    ProductDeleteView,
                    ProductDetailView,
                    ProductUpdateView,
                    HomeListView,
                    ContactView)

app_name = CatalogConfig.name

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('', HomeListView.as_view(), name='home'),
    path('home/', HomeListView.as_view(), name='home'),
    path('product/new/', ProductCreateView.as_view(), name='create_product'),
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
]
