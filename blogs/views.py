from django.shortcuts import render, redirect
from .models import Category, Articles
from django.views import View
# Create your views here.


class CategoryListView(View):
    def get(self, request):
        category = Category.objects.all()
        context = {
            'category' : category
        }
        return render(request, 'category_list.html', context=context)

