from django import forms
from .models import Category, Articles


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title', 'text')