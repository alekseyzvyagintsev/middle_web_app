from django.urls import path

from .apps import BlogConfig
from .views import (ActiveArticlesListView,
                    ArchiveArticlesListView,
                    BlogArticleCreateView,
                    BlogArticleDeleteView,
                    BlogArticleDetailView,
                    BlogArticleUpdateView,
                    ContactsView)

app_name = BlogConfig.name

urlpatterns = [
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("articles/list-is-active/", ActiveArticlesListView.as_view(), name="active_articles"),
    path("articles/archive_list/", ArchiveArticlesListView.as_view(), name="archive_articles"),
    path("article/new/", BlogArticleCreateView.as_view(), name="create_blog_article"),
    path("article/delete/<int:pk>/", BlogArticleDeleteView.as_view(), name="article_delete"),
    path("article/detail/<int:pk>/", BlogArticleDetailView.as_view(), name="article_detail"),
    path("article/update/<int:pk>/", BlogArticleUpdateView.as_view(), name="article_update"),
]
