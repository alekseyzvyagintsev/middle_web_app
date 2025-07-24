from django.urls import path
from .apps import BlogConfig
from .views import (BlogEntryCreateView,
                    IndexListView,
                    ContactsView,
                    BlogEntryDetailView,
                    BlogEntryDeleteView,
                    BlogEntryUpdateView)

app_name = BlogConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('index/', IndexListView.as_view(), name='index'),
    path('blogs/new/', BlogEntryCreateView.as_view(), name='create_blog_entry'),
#     path('product/list/', ProductListView.as_view(), name='product_list'),
    path('blogs/delete/<int:pk>/', BlogEntryDeleteView.as_view(), name='entry_delete'),
    path('blogs/detail/<int:pk>/', BlogEntryDetailView.as_view(), name='entry_detail'),
    path('blogs/update/<int:pk>/', BlogEntryUpdateView.as_view(), name='entry_update'),
]
