from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contact

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
]
