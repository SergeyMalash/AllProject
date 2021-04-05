from django import forms
from .models import Article
from django.core.exceptions import ValidationError
from django.db.models import Q


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'text')
    
