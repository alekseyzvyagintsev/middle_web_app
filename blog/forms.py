######################################################################################
from django import forms

from blog.models import BlogEntry


class ArticleForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ["title", "entry", "image", "is_active"]


######################################################################################
