from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Articles
from django.views import View
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import ArticlesForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser


# Create your views here.


class CategoryListView(View):
    def get(self, request):
        category = Category.objects.all()
        context = {
            'category': category
        }
        return render(request, 'blogs/category_list.html', context=context)


class ArticlesListView(View):
    def get(self, request, pk):
        articles = Articles.objects.filter(category=pk)
        context = {
            'articles': articles
        }
        return render(request, 'blogs/articles_list.html', context=context)


class ArticlesDetailView(View):
    def get(self, request, pk):
        article = Articles.objects.get(pk=pk)
        return render(request, 'blogs/articles_detail.html', {'article': article})


class ArticlesUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to edit this article.")

        update_article_form = ArticlesForm(instance=article)
        context = {
            'update_article_form': update_article_form,
            'article': article
        }
        return render(request, 'blogs/articles_update.html', context=context)

    def post(self, request, pk):
        article = get_object_or_404(Articles, pk=pk)
        if article.author != request.user:
            raise PermissionDenied("You are not allowed to edit this article.")

        update_article_form = ArticlesForm(request.POST, request.FILES, instance=article)
        if update_article_form.is_valid():
            update_article_form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('blogs:articles-detail', pk=article.pk)
        else:
            context = {
                'update_article_form': update_article_form,
                'article': article
            }
            return render(request, 'blogs/articles_update.html', context=context)

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
        return reverse_lazy('blogs:articles-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Article added successfully!")
        return response
