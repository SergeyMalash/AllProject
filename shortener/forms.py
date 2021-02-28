from django import forms
from .models import Url, Tag
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.db.models import Q


class UrlForm(forms.ModelForm):
    slug = forms.CharField(label='Сокращённый URL', required=False, max_length=50)
    tags = forms.ModelMultipleChoiceField(
        Tag.objects.none(),
        required=False,
        widget=forms.widgets.SelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(user__pk=request.user.pk)

    class Meta:
        model = Url
        fields = ('full', 'slug', 'tags')


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('title',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_title(self):
        """Проверяю уникальность тэга у конкретного user"""
        value = self.cleaned_data['title']
        if Tag.objects.filter(
                Q(user=self.request.user) &
                Q(title=value)):
            raise ValidationError("Такой тэг у Вас уже есть")
        return value


class SearchForm(forms.Form):
    search_text = forms.CharField()
