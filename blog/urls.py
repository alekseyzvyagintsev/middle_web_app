from django.urls import path
from .apps import BlogConfig
from .views import (BlogEntryCreateView,
                    ContactsView,
                    BlogEntryDetailView,
                    BlogEntryDeleteView,
                    BlogEntryUpdateView,
                    ActiveArticlesListView, ArchiveArticlesListView)

app_name = BlogConfig.name

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('articles/list-is-active/', ActiveArticlesListView.as_view(), name='active_articles'),
    path('articles/archive_list/', ArchiveArticlesListView.as_view(), name='archive_articles'),
    path('article/new/', BlogEntryCreateView.as_view(), name='create_blog_entry'),
    path('article/delete/<int:pk>/', BlogEntryDeleteView.as_view(), name='entry_delete'),
    path('article/detail/<int:pk>/', BlogEntryDetailView.as_view(), name='entry_detail'),
    path('article/update/<int:pk>/', BlogEntryUpdateView.as_view(), name='entry_update'),
]
