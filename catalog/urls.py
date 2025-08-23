######################################################################################
from django.urls import path

from .apps import CatalogConfig

from .views import (
    CategoryCreateView,
    CategoryDeleteView,
    CategoryDetailView,
    CategoryListView,
    CategoryUpdateView,
    ContactView,
    HomeListView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("contact/", ContactView.as_view(), name="contact"),
    path("", HomeListView.as_view(), name="home"),
    path("home/", HomeListView.as_view(), name="home"),
    path("category/mew/", CategoryCreateView.as_view(), name="create_category"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("category/delete/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
    path("category/detail/<int:pk>/", CategoryDetailView.as_view(), name="category_detail"),
    path("category/update/<int:pk>/", CategoryUpdateView.as_view(), name="category_update"),
    path("product/new/", ProductCreateView.as_view(), name="create_product"),
    path("products/", ProductListView.as_view(), name="products"),
    path("product/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("product/detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
]
######################################################################################
