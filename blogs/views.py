from django.shortcuts import render, redirect
from .models import Category, Articles
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ArticlesForm
from django.contrib import messages
# Create your views here.


class CategoryListView(View):
    def get(self, request):
        category = Category.objects.all()
        context = {
            'category' : category
        }
        return render(request, 'blogs/category_list.html', context=context)

class ArticlesListView(View):
    def get(self, request, pk):
        articles = Articles.objects.filter(category=pk)
        context = {
            'articles' : articles
        }
        return render(request, 'blogs/articles_list.html', context=context)


class ArticlesDetailView(View):
    def get(self, request, pk):
        article = Articles.objects.get(pk=pk)
        return render(request, 'blogs/articles_detail.html', {'article' : article})


class ArticlesUpdateView(UpdateView):
    model = Articles
    template_name = 'blogs/articles_update.html'
    fields = ['title', 'text']

    def get_success_url(self):
        return reverse_lazy('blogs:articles-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article updated successfully!")
        return response

class ArticlesCreateView(CreateView):
    model = Articles
    template_name = 'blogs/articles_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('blogs:articles-list', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article added successfully!")
        return response


